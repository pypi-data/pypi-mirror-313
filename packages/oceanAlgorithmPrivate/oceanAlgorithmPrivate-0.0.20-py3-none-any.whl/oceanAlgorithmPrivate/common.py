# -*- coding: utf-8 -*-
import oceanAlgorithmPrivate
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import json
import logging
import io
import boto3
import os
import matplotlib
import atexit
import warnings
from sklearn.preprocessing import label_binarize
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import roc_curve, auc
from botocore.exceptions import ClientError
from datetime import datetime
from sklearn.metrics import confusion_matrix
matplotlib.use('Agg')

class LoggerHelper:
    _shutdown_registered = False

    def __init__(self, log_level='DEBUG'):
        self.logger = self.setup_logger(log_level)
        
        if not LoggerHelper._shutdown_registered:
            atexit.register(self.log_shutdown_time)
            LoggerHelper._shutdown_registered = True

        warnings.filterwarnings("ignore")
        
    def setup_logger(self, log_level):
        logger = logging.getLogger('OceanAI_logger')
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        logger.propagate = False
        
        if not logger.hasHandlers():
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
        return logger
    
    def log_start_time(self):
        LoggerHelper.start_time = datetime.now()  # Set start time as a class-level attribute
        self.logger.info(f"시작 시간: {LoggerHelper.start_time}")

    def log_shutdown_time(self):
        end_time = datetime.now()
        if hasattr(LoggerHelper, 'start_time'):
            duration = end_time - LoggerHelper.start_time
            self.logger.info(f"종료 시간: {end_time}")
            self.logger.info(f"실행 시간: {duration}")
        else:
            self.logger.info(f"종료 시간: {end_time}")
    
    def check_verbose(self, log_level):
        if log_level == 'DEBUG':
            verbose = 2
        elif log_level == 'INFO':
            verbose = 1
        return verbose
    
    def log_parameters(self, **params):
        param_lines = []
        custom_labels = {
        'dep_var': '종속 변수',
        'indep_var': '독립 변수',
        'model': '모델 파라미터 정보'
        }
        split_info_keys = {'train_size', 'test_size', 'random_state', 
                           'X_train', 'y_train', 'X_test', 'y_test'}
        
        for key, value in params.items():
            if key in split_info_keys:
                if key == 'train_size':
                    param_lines.append(f"학습-테스트 데이터 분할 정보 \ntrain_size={value}")
                elif key == 'test_size':
                    param_lines.append(f"test_size={value}")
                elif key == 'random_state':
                    param_lines.append(f"random_state={value}")
                elif key == 'X_train':
                    param_lines.append(f"학습 데이터 크기\nX_train={value.shape}")
                elif key == 'y_train':
                    param_lines.append(f"y_train={value.shape}")
                elif key == 'X_test':
                    param_lines.append(f"테스트 데이터 크기\nX_test={value.shape}")
                elif key == 'y_test':
                    param_lines.append(f"y_test={value.shape}") 
            else:       
                if isinstance(value, pd.DataFrame):
                    formatted_value = self.format_dataframe(value)
                    label = custom_labels.get(key, '데이터 프레임')
                elif isinstance(value, pd.Series):
                    formatted_value = self.format_series(value)
                    label = custom_labels.get(key, '데이터 시리즈')
                elif isinstance(value, (dict, list)):
                    formatted_value = self.format_json(value)
                    label = custom_labels.get(key, 'JSON Parameter')
                elif hasattr(value, 'get_params'):
                    formatted_value = self.format_model_params(value)
                    label = custom_labels.get(key, '모델 파라미터')
                else:
                    formatted_value = str(value)
                    label = 'General Parameter'

                param_lines.append(f"\n{label} ({key})\n{formatted_value}")
                param_message = "\n\n".join(param_lines)
        param_message = "\n".join(param_lines)
        self.logger.debug(f"데이터 정보를 출력합니다.\n{param_message}")
    
    def format_dataframe(self, df):
        df_info = f"DataFrame Shape: {df.shape} \nColumns: {', '.join(df.columns)}"
        preview = df.head(5).to_string()
        return f"{df_info}\n데이터 미리보기\n{preview}"
    
    def format_series(self, series):
        series_info = f"Series Shape: {len(series)} \nName: {series.name if series.name else '없음'}"
        preview = series.head(5).to_string()
        return f"{series_info}\n데이터 미리보기\n{preview}"
    
    def format_json(self, obj):
        return json.dumps(obj, indent=4)
    
    def format_model_params(self, model):
        if self.logger.isEnabledFor(logging.INFO):
            additional_info = []
            attributes = [
                ('Search Type', model.__class__.__name__),
                ('Estimator', getattr(model, 'estimator', None)),
                ('Cross-Validation Folds', getattr(model, 'cv', None)),
                ('Input Parameters', getattr(model, 'param_grid', None)),
                ('Best Parameters', getattr(model, 'best_params_', None)),
                ('Best Score', getattr(model, 'best_score_', None)),
                ('Classes', getattr(model.best_estimator_, 'classes_', None) if hasattr(model, 'best_estimator_') else None),
                ('Classes Count', getattr(model.best_estimator_, 'class_count_', None) if hasattr(model, 'best_estimator_') else None),
                ('Classes Prior', getattr(model.best_estimator_, 'class_prior_', None) if hasattr(model, 'best_estimator_') else None)
            ]
            for name, value in attributes:
                if value is not None:
                    additional_info.append(f"{name}: {value}")
            return '\n'.join(additional_info)
    
    def log_event(self, event_type, status=None, fold=None, total_folds=None):
        if event_type == 'training':
            if status == 'started':
                self.start_time = datetime.now()
                self.logger.debug(f"모델 학습 시작")
            elif status == 'completed':
                self.end_time = datetime.now()
                self.logger.debug(f"모델 학습 완료")
                if self.start_time and self.end_time:
                    duration = self.end_time - self.start_time
                    self.logger.debug(f"모델 학습 소요 시간: {duration}")
                    
        elif event_type == 'prediction':
            if status == 'started':
                self.logger.debug("모델 예측 시작")
            elif status == 'completed':
                self.logger.debug("모델 예측 완료")
            elif status == 'created':
                self.logger.debug("모델 예측 결과 데이터 생성 완료")
                
        elif event_type == 'scaling':
            if status == 'started':
                self.logger.debug("데이터 스케일링 시작")
            elif status == 'completed':
                self.logger.debug("데이터 스케일링 완료")
                
        elif event_type == 'cross-validation':
            if status == 'started':
                self.logger.debug(f"교차 검증 시작 ({total_folds} folds)")
            elif status == 'completed':
                self.logger.debug("교차 검증 완료")
            elif status == 'fold_started' and fold and total_folds:
                self.logger.debug(f"Fold {fold}/{total_folds} - 교차 검증 시작")
            elif status == 'fold_completed' and fold and total_folds:
                self.logger.debug(f"Fold {fold}/{total_folds} - 교차 검증 완료")


class Private(LoggerHelper):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Private, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, log_level='DEBUG'):
        if not hasattr(self, 'initialized') or not self.initialized:
            super().__init__(log_level=log_level)
            
            try:
                print(f"oceanAlgorithmPrivate version: {oceanAlgorithmPrivate.__version__}")
            except AttributeError:
                print("oceanAlgorithmPrivate does not have a __version__ attribute.")
            
            self.session = boto3.session.Session()
            self.client = self.session.client('secretsmanager', region_name='ap-northeast-2')
            self.s3 = boto3.client('s3')
            self.bucket_name = None
            self.s3_path = None
            self.base_filename = None

            self.raw_data = None
            self.raw_info = None
            
            self.features_ticker_property = None
            self.target_ticker_property = None
            self.initialized = True
            
    def get_secret(self, db_name):
        secret_name = 'dev/' + db_name + '/data/postgres'
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
            secret_value = json.loads(get_secret_value_response['SecretString'])
            return secret_value
        except ClientError as e:
            print(f'ClientError: {e}')
            return None
    
    def set_s3_info(self, param_info):
        self.s3_info = param_info['s3_info']
        self.s3_path = self.s3_info['s3_write_path']
        self.base_filename = self.s3_info['filename']
        self.bucket_name = self.s3_info['s3_repository']
    
    def upload_to_s3(self, file_name, bucket_name, s3_path):
        try:
            self.s3.upload_file(file_name, bucket_name, s3_path)
        except Exception as e:
            self.logger.error(f"Failed to upload {file_name}")
    
    def upload_bytes_to_s3(self, byte_stream, file_name, bucket_name, s3_path):
        try:
            byte_stream.seek(0)
            self.s3.upload_fileobj(byte_stream, bucket_name, s3_path)
        except boto3.exception.S3UploadFailedError as e:
            self.logger.error(f"Upload failed for file-like object {file_name}. Error: {e}")
        except Exception as e:
            self.logger.error(f"Failed to upload file-like object {file_name} to S3: {e}")
    
    def upload_file(self,files,var_names=None, target_name=None):
        if not isinstance(files, list):
            files = [files]
            
        if not isinstance(var_names, list):
            var_names = [var_names]
            
        if var_names is None:
            var_names = [None] * len(files)
        elif not isinstance(var_names, list):
            var_names = [var_names]
        elif len(var_names) != len(files):
            raise ValueError("The length of 'var_names' must match the length of 'files'.")
            
        for file_obj, var_name in zip(files, var_names):
            suffix = f"_{var_name}" if var_name else ""
            
            if target_name:
                file_name = f"{self.base_filename}_{target_name}{suffix}"
            else:
                file_name = f"{self.base_filename}{suffix}"
                
            if isinstance(file_obj, pd.DataFrame):
                file_name += ".csv"
                file_obj = self.add_dtype(file_obj)
                file_obj.to_csv(file_name, index=None, encoding='utf-8')
                self.upload_to_s3(file_name, self.bucket_name, self.s3_path + file_name)
                
            elif isinstance(file_obj, dict):
                file_name += ".json"
                self.save_to_json(file_obj, file_name)
                self.upload_to_s3(file_name, self.bucket_name, self.s3_path + file_name)
                
            elif isinstance(file_obj, plt.Figure):
                file_name += ".png"
                img_bytes = io.BytesIO()
                file_obj.savefig(img_bytes, format='png')
                img_bytes.seek(0)
                self.upload_bytes_to_s3(img_bytes, file_name, self.bucket_name, self.s3_path + file_name)

            if file_name:
                self.cleanup_files([file_name])
    
    def cleanup_files(self, file_names):
        for file_name in file_names:
            if os.path.exists(file_name):
                os.remove(file_name)

    def read_csv(self,file_path):
        raw = pd.read_csv(file_path)
        dtype_dict = {col: dtype for col, dtype in zip(raw.columns, list(raw.iloc[0]))}
        df = raw.iloc[1:]
        df = df.astype(dtype_dict)
        
        first_column_name = df.columns[0]
        df.set_index(first_column_name, inplace=True)
        df = df.dropna(how='any')
        return df, dtype_dict
    
    
    def read_data(self, file_path, json_data, schema_json, variable=None):
        self.raw_info = schema_json
        self.raw_data, dtype_dict = self.read_csv(file_path)
        X, y = None, None
    
        if schema_json:
            df = self.raw_data.copy()
        else:
            error_message = "데이터 속성 정보가 없어서 프레임 재구성을 할 수 없습니다."
            self.logger.error(error_message)
            sys.exit(1)
        # 데이터 검증
        try:
            if variable is not None:
                X, y = self.validate_dataframe(df, dtype_dict, json_data, variable)
                return X, y
            else:
                return df
        except Exception as e:
            error_message = f"데이터 검증 중 예기치 못한 오류가 발생했습니다"
            self.logger.error(error_message)
            sys.exit(1)
        return X, y
    
    def validate_dataframe(self, df, dtype_dict, json_data, variable):
        column_schema = {
            item['name']: {
                'ticker': item.get('ticker', None),
                'property': item.get('property', None),
                'description': item.get('description', None),
            }
            for item in self.raw_info['columns']
        }
        # 데이터 타입 검증
        column_valid = self.validate_selected_column(df, dtype_dict, json_data, variable)
        # 종속변수 확인
        target_columns = variable['dep_var']
        target_columns = target_columns if isinstance(target_columns, list) else [target_columns]
        # 스케일링 피처 검증
        features_columns_scaled = self.validate_scaling_columns(column_schema, variable)

        if column_valid:
            try:
                X, y = self.validate_common_columns(df, column_schema, features_columns_scaled, target_columns)
            except Exception as e:
                error_message = f"데이터 검증 중 예기치 못한 오류가 발생했습니다"
                self.logger.error(error_message)
                sys.exit(1)
        else:
            error_message = "데이터 검증에 실패했습니다."
            self.logger.error(error_message)
            sys.exit(1)
        return X, y
    
    def map_ticker_properties(self, columns, column_schema):
        # 티커별 속성 매핑
        ticker_property_map = {}
        for column in columns:
            column_info = column_schema[column]
            ticker = column_info['ticker']
            property_name = column_info['property']
            
            if ticker not in ticker_property_map:
                ticker_property_map[ticker] = set()
            ticker_property_map[ticker].add(property_name)
        return ticker_property_map
    
    def validate_common_columns(self, df, column_schema, features_columns, target_columns):
        self.features_ticker_property = self.map_ticker_properties(features_columns, column_schema) # indep_var
        self.target_ticker_property = self.map_ticker_properties(target_columns, column_schema) # dep_var
        
        # 종속변수 갯수 확인
        num_target_column = len(target_columns)
        num_target_ticker = len(self.target_ticker_property)
        
        # 1. 종속변수 == 1개 -> 그대로 학습함
        if num_target_column == 1:
            X = df[features_columns]
            y = df[target_columns]
            return X, y
        
        if num_target_column > 1 and num_target_ticker > 1:
            # 공통 티커와 속성 찾기
            common_properties_features = set.intersection(*self.features_ticker_property.values()) # 피처 공통 속성(indep_var)
            common_properties_target = set.intersection(*self.target_ticker_property.values()) # 타겟 공통 속성(dep_var)
            
            # 종속변수 속성이 1개인지 확인
            if len(common_properties_target) != 1:
                error_message = "종속변수의 공통 속성이 1개가 아닙니다. 학습을 중단합니다."
                self.logger.error(error_message)
                sys.exit(1)
                
            # 종속변수와 독립변수의 공통티커 확인
            if set(self.features_ticker_property.keys()) != set(self.target_ticker_property.keys()):
                error_message = (f"종속변수와 독립변수가 동일 티커에 대한 값을 포함하고 있지 않습니다. 학습을 중단합니다."
                         f"종속변수 티커: {', '.join(self.target_ticker_property.keys())}, "
                         f"독립변수 티커: {', '.join(self.features_ticker_property.keys())}")
                self.logger.error(error_message)
                sys.exit(1)
            
            # 피처 중에서 공통 속성 확인
            final_features_columns = []
            for feature in features_columns:
                if feature in column_schema:
                    feature_info = column_schema[feature]
                    feature_property = feature_info['property']
                    
                    if (feature_property in common_properties_features):
                        final_features_columns.append(feature)
            
            # 선택된 독립변수와 종속변수 반환
            X = df[final_features_columns]
            y = df[target_columns]
            return X, y
    
    def reshape_for_model(self, X_train, y_train, X_test=None, y_test=None):
        feature = X_train.columns
        target = y_train.columns
        
        if X_test is None and y_test is None:
            if len(target) == 1:
                return X_train, y_train.squeeze()
            train_data = pd.concat([X_train, y_train], axis=1)
            X_train_data, y_train_data = self.reshape_frame(train_data, feature, target)
            return X_train_data, y_train_data
        
        else:
            if len(target) == 1:
                return X_train, y_train.squeeze(), X_test, y_test.squeeze()
            train_data = pd.concat([X_train, y_train], axis=1)
            test_data = pd.concat([X_test, y_test], axis=1)
        
            # reshape -> model에 입력되는 형태로 재가공
            X_train_data, y_train_data = self.reshape_frame(train_data, feature, target)
            X_test_data, y_test_data = self.reshape_frame(test_data, feature, target)
        
            return X_train_data, y_train_data, X_test_data, y_test_data
    
    def validate_scaling_columns(self, column_schema, variable):
        features = variable['indep_var']
        excluded_scaling_columns = []
        selected_columns = []

        # 피처 컬럼에서 스케일링된 컬럼 제외
        for column in features:
            column_info = column_schema[column]
            if 'scaling' in column_info['description'].lower():
                excluded_scaling_columns.append(column)
            else:
                selected_columns.append(column) # 스케일링 컬럼 제외한 타겟 컬럼
        # validation
        if not selected_columns:
            error_message = "선택된 독립변수는 스케일링이 적용된 데이터이므로 데이터 리키지를 방지하기 위해 학습을 중단합니다."
            self.logger.error(error_message)
            sys.exit(1)
        else:
            if excluded_scaling_columns:
                warning_message =f"주의: 이미 스케일링이 적용된 컬럼은 학습 대상에서 제외됩니다: {', '.join(excluded_scaling_columns)}"
                self.logger.warning(warning_message)
        return selected_columns    

    def select_scaler(self, scaler_option):
        if scaler_option == 'minmax':
            scaler = MinMaxScaler()
        elif scaler_option == 'standard':
            scaler = StandardScaler()
        else:
            scaler = None  # No scaling
        return scaler
    
    def scale_data(self, scaler, train_set, test_set=None):
        if scaler is None:
            if test_set is None:
                return train_set
            else:
                return train_set, test_set
        else:
            if test_set is None:
                train_scaled = pd.DataFrame(scaler.fit_transform(train_set), index=train_set.index, columns=train_set.columns)
                return train_scaled
            else:
                train_scaled = pd.DataFrame(scaler.fit_transform(train_set), index=train_set.index, columns=train_set.columns)
                test_scaled = pd.DataFrame(scaler.transform(test_set), index=test_set.index, columns=test_set.columns)
                return train_scaled, test_scaled

    def reshape_frame(self, df, indep_vars, dep_vars):
        var_info = self.raw_info
        dep_var_info, indep_var_info = [], []

        for label_col in dep_vars:
            for column in var_info['columns']:
                if column['name'] == label_col:
                    dep_var_info.append(column)
        
        for label_col in indep_vars:
            for column in var_info['columns']:
                if column['name'] == label_col:
                    indep_var_info.append(column)        

        dep_tickers = set(info['ticker'] for info in dep_var_info)
        indep_tickers = set(info['ticker'] for info in indep_var_info)
        
        dep_df = self.build_rows(df, dep_tickers, dep_var_info).squeeze()
        indep_df = self.build_rows(df, indep_tickers, indep_var_info)
        return indep_df, dep_df
    
    def build_rows(self, df, tickers, target_var_info):
        # var_info에서 ticker와 property 정보를 기반으로 재구성
        rows = []
        index_name = df.index.name
        for date in df.index:
            for ticker in tickers:
                row = {'ticker': ticker, index_name: date}
                for info in target_var_info:
                    if info['ticker'] == ticker:
                        col_name = info['name']
                        prop_name = info['property']
                        
                        row[prop_name] = df.at[date, col_name]
                rows.append(row)
                
        result_df = pd.DataFrame(rows).set_index([df.index.name, 'ticker']).sort_index()
        return result_df

    
    def merge_result(self, X_test, df_result): # input 수정
        original_df = self.raw_data.copy()
        df_result = pd.concat([X_test, df_result], axis=1)
        
        column_properties = ['y_true', 'y_pred']
        if 'y_prob' in df_result.columns:
            column_properties.append('y_prob') # 분류 모델일 경우 확률 값 추가
            
        if len(self.target_ticker_property.keys()) == 1:
            target_ticker = next(iter(self.target_ticker_property.keys()))
            
            rename_mapping = {}
            for prop in column_properties:
                if prop in df_result.columns:
                    # 각 속성에 target_ticker를 추가하여 새 이름을 생성
                    new_column_name = f"{target_ticker}_{prop}"
                    rename_mapping[prop] = new_column_name
            df_result = df_result.rename(columns=rename_mapping)
            return df_result
        
        df_result = df_result.reset_index().set_index(original_df.index.name)
        
        if 'ticker' in df_result.columns: # ticker 컬럼 여부 확인
            unique_tickers = df_result['ticker'].unique()
            for ticker in unique_tickers:
                df_ticker = df_result[df_result['ticker'] == ticker]
                for base_col_name in column_properties:
                    col_name = f'{ticker}_{base_col_name}'
                    original_df.loc[df_ticker.index, col_name] = df_ticker[base_col_name].values
        else:
            for base_col_name in column_properties:
                original_df[base_col_name] = df_result[base_col_name].values

        original_df = original_df.loc[original_df.index.isin(df_result.index)]
        return original_df
    
        
    def save_results(self, variable, report=None, fig=None):
        target_name = variable['dep_var']
        uploaded_files = []  # 업로드된 파일들을 추적하기 위한 리스트
        var_names = []  # 업로드 파일의 변수 이름
       
        # eval_report 업로드
        if report is not None:
            uploaded_files.append(report)
            var_names.append('report')
 
        # fig 업로드
        if fig is not None:
            uploaded_files.append(fig)
            var_names.append('fig')
       
        # 업로드 파일이 있는 경우에만 파일 업로드
        if uploaded_files:
            self.upload_file(uploaded_files, var_names=var_names, target_name=target_name)
           
        if fig is not None:
            print(f"{self.base_filename}_{target_name}_fig.png")
 
        self.log_event('prediction', status='created')

        
    def generate_schema_json(self, params, schema_json, func_name=None):
        self.set_s3_info(params)
        variables = params.get('variables', [])
        column_properties = {
            'y_true': {'property': 'true_value', 'data_type': 'int64'},
            'y_pred': {'property': 'predictive_value', 'data_type': 'float64'},
            'y_prob': {'property': 'probability', 'data_type': 'int64'}
        }
        for variable in variables:
            dep_var = variable.get('dep_var')
            
            for column in schema_json['columns']:
                if column['name'] == dep_var:
                    ticker = column['ticker']
                    ticker_type = column['ticker_type']
                    
                    for prefix, properties in column_properties.items():
                        col_name = f"{ticker}_{prefix}"
                        param = {
                            "name": col_name,
                            "ticker": ticker if ticker else "",
                            "ticker_type": ticker_type,
                            "property": properties['property'],
                            "description": f"{properties['property']}",
                            "data_type": properties['data_type'],
                            "created_by": func_name
                            }
                        schema_json['columns'].append(param)
        
        self.upload_file(schema_json)
        return schema_json

    def add_dtype(self,df):
        if type(df.index) == pd.core.indexes.range.RangeIndex:
            pass
        else:
            df = df.reset_index()
        column_and_type = [(col, df[col].dtype) for col in df.columns]
        df.columns = pd.MultiIndex.from_tuples(column_and_type)
        return df
    
    def parse_json(self,json_string: str) -> dict:
        try:
            data_dict = json.loads(json_string)
            return data_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {}
    
    def read_json(self, file_path):
        if not os.path.exists(file_path):
            error_message = f"데이터 속성 파일 '{file_path}'이 존재하지 않습니다."
            self.logger.error(error_message)
            sys.exit(1)
        # JSON 파일 로드
        try:
            with open(file_path, 'r') as file:
                params = json.load(file)
                self.logger.info(f"데이터 속성 파일 '{file_path}'이 로드되었습니다.")
                return params
        except json.JSONDecodeError as e:
            error_message = f"데이터 속성 파일 '{file_path}'을 파싱하는 동안 오류가 발생했습니다: {e}"
            self.logger.error(error_message)
            sys.exit(1)
        except Exception as e:
            error_message = f"데이터 속성 파일 '{file_path}'을 읽는 동안 예상치 못한 오류가 발생했습니다: {e}"
            self.logger.error(error_message)
            sys.exit(1)
    
    def generate_report(self, INPUT=None, accuracy=None, report=None, matrix=None, auc_score=None, mse=None, rmse=None, mae=None, r2=None):
        pred_type = INPUT.get('pred_type', None)
        if pred_type != 'reg': # 로지스틱의 경우 pred_type이 없음
            # Classification Report Generation
            report_df = pd.DataFrame(report).transpose().reset_index().rename(columns={'index': 'Class'})
            class_labels = report_df['Class'][:len(matrix)].tolist()
            num_classes = matrix.shape[1]
            column_names = [f'Predicted {i}' for i in range(num_classes)]

            matrix_df = pd.DataFrame(matrix, columns=column_names)
            matrix_df['Class'] = class_labels
            matrix_df = matrix_df[['Class'] + column_names]

            combined_df = pd.merge(report_df, matrix_df, on='Class', how='left')

            metrics_df = pd.DataFrame({
                'Class': ['Accuracy', 'AUC Score'],
                'Score': [accuracy, auc_score],
                'precision': [None, None],
                'recall': [None, None],
                'f1-score': [None, None],
                'support': [None, None],
                'Predicted 0': [None, None],
                'Predicted 1': [None, None]
            })

            for col in column_names:
                metrics_df[col] = [None, None]

            final_df = pd.concat([metrics_df, combined_df], ignore_index=True)
            final_df = final_df.set_index('Class')

        else:
            # Regression Report Generation
            final_df = pd.DataFrame({
                'Metric': ['Mean Squared Error (MSE)', 'Root Mean Squared Error (RMSE)', 
                        'Mean Absolute Error (MAE)', 'R2 Score'],
                'Score': [mse, rmse, mae, r2]
            })

        final_df = final_df.fillna(' ')
        self.log_event('evaluation', status='completed')
        self.log_parameters(evaluation_report=final_df)
        return final_df
    
    def save_to_json(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    def confusion_matrix(self,y, y_pred):
        classes = sorted(y.unique())
        matrix = confusion_matrix(y, y_pred, labels=classes)
        df = pd.DataFrame(matrix, columns=[f'Predicted {cls}' for cls in classes], index=[f'Actual {cls}' for cls in classes])
        return df
    
    def roc_curve(self, y, probabilities):
        classes = sorted(list(set(y)))
        n_classes = len(classes)
        plt.figure(figsize=(8, 6))
        
        if n_classes > 2:
            y_bin = label_binarize(y, classes=classes)
        
            for i, class_name in enumerate(classes):
                y_prob = probabilities[:, i]
                fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob) # ROC 곡선 계산
                auc_score = auc(fpr, tpr) # AUC 값 계산
                plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'{class_name} (AUC = {auc_score:.2f})')
                
        else:  # Binary case
            y_prob = probabilities[:, 1]
            fpr, tpr, _ = roc_curve(y, y_prob)
            auc_score = auc(fpr, tpr)
            class_name = classes[1]
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'{class_name} (AUC = {auc_score:.2f})')
                
            plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'ROC Curve for {y.name}')
            plt.legend(loc="lower right")

        fig = plt.gcf()
        plt.close()  
        return fig, auc_score

    def get_parameters(self, json_data):
        parameters = {
            'model_par': {},
            's3_info':{}
            }
        
        s3_storage = json_data['s3_storage']
        node_information = json_data['node_information']
        parameters['s3_info']['s3_repository'] = s3_storage.get('s3_repository', None)
        parameters['s3_info']['s3_write_path'] = s3_storage.get('s3_write_path', None)
        parameters['s3_info']['filename'] = node_information.get('user_defined_name', None)

        
        for parameter in json_data['parameters']:
            area = parameter['area']
            options = parameter.get('options')
            parameter_name = parameter['parameter_name']
            selected_value = parameter.get('selected_value')
            value_type = parameter.get('value_type')
                                       
            if options:
                if area == 'hyperparameter':
                    if selected_value == 'values':
                        values_option = next((opt for opt in options if opt['value'] == 'values'), None)
                        if values_option:
                            parameter_value  = [member['selected_value'] for member in values_option['members']]
                            if len(parameter_value) == 1:
                                parameter_value = parameter_value[0]
                    elif selected_value == 'range':
                        range_option = next((opt for opt in options if opt['value'] == 'range'), None)
                        if range_option:
                            range_members = range_option['members']
                            range_values = {member['name']: member['selected_value'] for member in range_members}
                            value_types = {member['name']: member['value_type'] for member in range_members}

                            min_val = range_values['min']
                            max_val = range_values['max']
                            count = range_values['count']
                            dist = range_values['dist']
                            
                            if dist == 'uniform':
                                if value_types['min'] == 'integer' and value_types['max'] == 'integer':
                                    parameter_value = np.linspace(min_val, max_val, count).astype(int).tolist()
                                else:
                                    parameter_value = np.linspace(min_val, max_val, count).tolist()
                            elif dist == 'log_uniform':
                                min_val = float(min_val)
                                max_val = float(max_val)
                                parameter_value = np.logspace(np.log10(min_val), np.log10(max_val), count).tolist()
                            else:
                                parameter_value = None
                        else:
                            parameter_value = None
                    else:
                        if isinstance(selected_value, list) and len(selected_value) == 1:
                            parameter_value = selected_value[0] 
                        else:
                            parameter_value = selected_value
                    parameters['model_par'][parameter_name] = parameter_value
                
                elif value_type == "dict":
                    if isinstance(selected_value, list) and all(isinstance(item, dict) for item in selected_value):
                        dict_values = [
                            {'dep_var': item.get('dep_var'), 'indep_var': item.get('indep_var')}
                            for item in selected_value
                        ]
                        parameters['model_par'][parameter_name] = dict_values
                    else:
                        parameters['model_par'][parameter_name] = selected_value
                else:
                    parameters[parameter_name] = selected_value
            else:
                parameters[parameter_name] = selected_value
        return parameters

    
    def validate_data(self,json_data):
        # 스키마 검증
        if isinstance(json_data, str):
            error_message = "데이터 속성 파일이 존재하지 않습니다."
            self.logger.error(error_message)
            sys.exit(1)
        # 데이터 타입 검증
        is_value_valid = self.validate_selected_value(json_data)
        
        if is_value_valid:
            self.logger.info("데이터 유효성 검사가 성공했습니다.")
            return True
        else:
            error_message = "데이터 유효성 검사가 실패했습니다."
            self.logger.error(error_message)
            sys.exit(1)
            
    def get_pred_type(self, json_data):
        for item in json_data['parameters']:
            if item.get('parameter_name') == 'pred_type':
                return item.get('selected_value')
        return None
    
    def is_dtype_match(self, column, allowed_types, df):
        if 'int' in allowed_types and pd.api.types.is_integer_dtype(df[column]):
            return True
        if 'float' in allowed_types and pd.api.types.is_float_dtype(df[column]):
            return True
        if 'string' in allowed_types and pd.api.types.is_string_dtype(df[column]):
            return True
        if 'datetime' in allowed_types and pd.api.types.is_datetime64_any_dtype(df[column]):
            return True
        return False
        
    def validate_selected_column(self, df, dtype_dict, json_data, variable):
        variables_param = None
        pred_type = self.get_pred_type(json_data)
        pred_type_display_map = {"reg": "회귀", "class_binary": "이진분류", 'class_multi': '다중분류'}
        
        overall_valid = True
        
        for param in json_data['parameters']:
            if param.get('parameter_name') == 'variables':
                variables_param = param
                break
            
        for item in variables_param['members']:
            param_name = item['name']
            allowed_types = item.get('allowed_data_types', [])
            columns_to_check = variable[param_name]
            display_name = item.get('ui_display_name_ko', param_name)
            # unique_value_constraints = item.get('n_unique_value', [])

            unique_value_constraints = [
                constraint for constraint in item.get('n_unique_value', [])
                if constraint.get('pred_type') == pred_type
            ]
            columns_to_check = columns_to_check if isinstance(columns_to_check, list) else [columns_to_check]
            
            param_valid = True
            for col_name in columns_to_check:
                # 컬럼 존재 여부 확인
                if col_name not in dtype_dict:
                    print(f"데이터 프레임에 '{col_name}' 열이 존재하지 않습니다.")
                    param_valid = False
                    continue
                
                if not self.is_dtype_match(col_name, allowed_types, df):
                    print(f"'{display_name}'의 '{col_name}'열의 데이터 유형이 허용된 유형({allowed_types})과 일치하지 않습니다.")
                    param_valid = False
                    
                # pred_type의 unique_value 조건 조회
                unique_count = df[col_name].nunique()
                for constraint in unique_value_constraints:
                    min_val, max_val = constraint['min'], constraint['max']
                    pred_type_display = pred_type_display_map.get(pred_type, pred_type)
                    
                    if max_val == 'inf': # 회귀
                        if unique_count < min_val:
                            if pred_type_display:
                                print(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 '{pred_type_display}'에 대한 최소 허용값({min_val})을 벗어납니다.")
                            else:
                                print(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 최소 허용값({min_val})을 벗어납니다.")
                            param_valid = False
                    else:
                        if not (min_val <= unique_count <= max_val):
                            if pred_type_display:
                                print(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 '{pred_type_display}'에 대한 허용 범위(최소값:{min_val}, 최대값:{max_val})를 벗어납니다.")
                            else:
                                print(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 허용 범위(최소값:{min_val}, 최대값:{max_val})를 벗어납니다.")
                            param_valid = False
                            
            if not param_valid:
                overall_valid = False
        return overall_valid
    
    def validate_selected_value(self, json_data):
        for data in json_data['parameters']:
            value_type = data.get("value_type")
            selected_value = data.get("selected_value")
            ui_display_name = data.get("ui_display_name_ko")
            
            if value_type == "float":
                if not isinstance(selected_value, float):
                    error_message = f"오류: '{ui_display_name}'의 값이 실수 타입이 아닙니다. 실수형 값을 입력해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
            elif value_type == "integer":
                if not isinstance(selected_value, int):
                    error_message = f"오류: '{ui_display_name}'의 값이 정수 타입이 아닙니다. 정수형 값을 입력해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
            elif value_type == "string":
                if not isinstance(selected_value, str):
                    error_message = f"오류: '{ui_display_name}'의 값이 문자열 타입이 아닙니다. 문자 형태의 값을 입력해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
            elif value_type == "float_array":
                if not isinstance(selected_value, list):
                    error_message = f"오류: '{ui_display_name}'의 값이 리스트 형태가 아닙니다. 리스트 형태로 실수형 값을 입력해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
                if not all(isinstance(item, float) for item in selected_value):
                    error_message = f"오류: '{ui_display_name}'의 리스트 내 모든 요소가 실수 타입이 아닙니다. 모든 요소가 실수형인지 확인해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
            elif value_type == "integer_array":
                if not isinstance(selected_value, list):
                    error_message = f"오류: '{ui_display_name}'의 값이 리스트 형태가 아닙니다. 리스트 형태로 정수형 값을 입력해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
                if not all(isinstance(item, int) for item in selected_value):
                    error_message = f"오류: '{ui_display_name}'의 리스트 내 모든 요소가 정수 타입이 아닙니다. 모든 요소가 정수형인지 확인해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)

            elif value_type == "string_array":
                if not isinstance(selected_value, list):
                    error_message = f"오류: '{ui_display_name}'의 값이 리스트 형태가 아닙니다. 리스트 형태로 문자열을 입력해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
                if not all(isinstance(item, str) for item in selected_value):
                    error_message = f"오류: '{ui_display_name}'의 리스트 내 모든 요소가 문자열 타입이 아닙니다. 모든 요소가 문자열인지 확인해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
            
            elif value_type == 'dict':
                if not isinstance(selected_value, list) or not all(isinstance(item, dict) for item in selected_value):
                    error_message = f"오류: '{ui_display_name}'의 값이 딕셔너리 리스트 형태가 아닙니다. 딕셔너리 리스트 형태로 입력해 주세요."
                    self.logger.error(error_message)
                    sys.exit(1)
                # 각 딕셔너리에 필수 키 확인
                for item in selected_value:
                    if 'dep_var' not in item or 'indep_var' not in item:
                        error_message = f"오류: '{ui_display_name}' 항목에 '종속변수' 또는 '독립변수'가 누락되었습니다."
                        self.logger.error(error_message)
                        sys.exit(1)
            else:
                error_message = f"오류: '{ui_display_name}'의 데이터 타입('{value_type}')은 지원되지 않는 타입입니다. 올바른 유형인지 확인해 주세요."
                self.logger.error(error_message)
                sys.exit(1)

            value_range = data.get("value_range")
            if value_range:
                min_value = value_range.get("min")
                max_value = value_range.get("max")
            
                if min_value is None or max_value is None:
                    error_message = f"오류: '{ui_display_name}'에 최소값 또는 최대값이 누락되었습니다."
                    self.logger.error(error_message)
                    sys.exit(1)
        
                if isinstance(selected_value, list):
                    if not all(min_value <= item <= max_value for item in selected_value):
                        error_message = f"오류: '{ui_display_name}'의 한 개 이상의 요소가 범위 [최소값:{min_value}, 최대값:{max_value}]를 벗어납니다."
                        self.logger.error(error_message)
                        sys.exit(1)
                else:
                    if not (min_value <= selected_value <= max_value):
                        error_message = f"오류: '{ui_display_name}'의 값이({selected_value}) 범위 [최소값:{min_value}, 최대값:{max_value}]을 벗어납니다."
                        self.logger.error(error_message)
                        sys.exit(1)
        return True
    
    def residual_diag_plot(self, fitted, residual):
        plt.figure(figsize=(8, 6))
       
        plt.scatter(fitted, residual)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Fitted Values (Predicted)')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
       
        fig = plt.gcf()
        plt.close()
        return fig