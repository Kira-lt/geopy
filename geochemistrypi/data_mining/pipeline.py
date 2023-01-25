# -*- coding: utf-8 -*-
import os
from .global_variable import OPTION, SECTION, IMPUTING_STRATEGY, MODE_OPTION, REGRESSION_MODELS,\
    CLASSIFICATION_MODELS, CLUSTERING_MODELS, DECOMPOSITION_MODELS, WORKING_PATH, DATA_OPTION,\
    TEST_DATA_OPTION, MODEL_OUTPUT_IMAGE_PATH, STATISTIC_IMAGE_PATH, DATASET_OUTPUT_PATH,\
    GEO_IMAGE_PATH, MAP_IMAGE_PATH, MODEL_PATH, NON_AUTOML_MODELS
from .data.data_readiness import read_data, show_data_columns, num2option, create_sub_data_set, basic_info, np2pd, \
    num_input, limit_num_input
from .data.imputation import imputer
from .data.feature_engineering import FeatureConstructor
from .data.statistic import monte_carlo_simulator
from .plot.statistic_plot import basic_statistic, correlation_plot, distribution_plot, is_null_value, probability_plot, \
    ratio_null_vs_filled, logged_distribution_plot, is_imputed
from .plot.map_plot import map_projected
from .utils.base import clear_output, log, show_warning
from .process.regress import RegressionModelSelection
from .process.classify import ClassificationModelSelection
from .process.cluster import ClusteringModelSelection
from .process.decompose import DecompositionModelSelection

# create the directories if they didn't exist yet
os.makedirs(MODEL_OUTPUT_IMAGE_PATH, exist_ok=True)
os.makedirs(STATISTIC_IMAGE_PATH, exist_ok=True)
os.makedirs(DATASET_OUTPUT_PATH, exist_ok=True)
os.makedirs(MAP_IMAGE_PATH, exist_ok=True)
os.makedirs(GEO_IMAGE_PATH, exist_ok=True)
os.makedirs(MODEL_PATH, exist_ok=True)


def pipeline(file_name: str) -> None:
    print("Geochemistry Py - User Behaviour Testing Demo")
    print("....... Initializing .......")
    logger = log(WORKING_PATH, "test.log")
    logger.info("Geochemistry Py - User Behaviour Testing Demo")

    # If the argument is False, hide all Python level warnings.
    show_warning(False)

    # Read the data
    logger.debug("Data Uploaded")
    print("-*-*- Data Loading -*-*-")
    if file_name:
        data = read_data(file_name=file_name, is_own_data=1)
        print(f"Successfully load the data set '{file_name}'.")
    else:
        print("Built-in Data Option:")
        num2option(TEST_DATA_OPTION)
        test_data_num = limit_num_input(TEST_DATA_OPTION, SECTION[0], num_input)
        if test_data_num == 1:
            file_name = 'Data_Regression.xlsx'
        elif test_data_num == 2:
            file_name = 'Data_Classification.xlsx'
        elif test_data_num == 3:
            file_name = 'Data_Clustering.xlsx'
        elif test_data_num == 4:
            file_name = 'Data_Decomposition.xlsx'
        data = read_data(file_name=file_name)
        print(f"Successfully loading the built-in data set '{file_name}'.")
    show_data_columns(data.columns)
    clear_output()

    # World map projection for a specific element
    logger.debug("World Map Projection")
    map_flag = 0
    is_map_projection = 0
    while True:
        if map_flag != 1:
            # option selection
            print("World Map Projection for A Specific Element Option:")
            num2option(OPTION)
            is_map_projection = limit_num_input(OPTION, SECTION[3], num_input)
            clear_output()
        if is_map_projection == 1:
            print("-*-*- Distribution in World Map -*-*-")
            print("Select one of the elements below to be projected in the World Map: ")
            show_data_columns(data.columns)
            elm_num = limit_num_input(data.columns, SECTION[3], num_input)
            map_projected(data.iloc[:, elm_num - 1], data)
            clear_output()
            print("Do you want to continue to project a new element in the World Map?")
            num2option(OPTION)
            map_flag = limit_num_input(OPTION, SECTION[3], num_input)
            if map_flag == 1:
                clear_output()
                continue
            else:
                print('Exit Map Projection Mode.')
                clear_output()
                break
        elif is_map_projection == 2:
            break

    # Create the processing data set
    logger.debug("Data Selected")
    print("-*-*- Data Selected -*-*-")
    show_data_columns(data.columns)
    data_processed = create_sub_data_set(data)
    clear_output()
    print("The Selected Data Set:")
    print(data_processed)
    clear_output()
    print('Basic Statistical Information: ')
    basic_info(data_processed)
    basic_statistic(data_processed)
    correlation_plot(data_processed.columns, data_processed)
    distribution_plot(data_processed.columns, data_processed)
    logged_distribution_plot(data_processed.columns, data_processed)
    clear_output()

    # Imputing
    logger.debug("Imputation")
    is_null_value(data_processed)
    ratio_null_vs_filled(data_processed)
    imputed_flag = is_imputed(data_processed)
    clear_output()
    if imputed_flag:
        print("-*-*- Strategy for Missing Values -*-*-")
        num2option(IMPUTING_STRATEGY)
        print("Which strategy do you want to apply?")
        strategy_num = limit_num_input(IMPUTING_STRATEGY, SECTION[1], num_input)
        data_processed_imputed_np = imputer(data_processed, IMPUTING_STRATEGY[strategy_num - 1])
        data_processed_imputed = np2pd(data_processed_imputed_np, data_processed.columns)
        clear_output()
        print("-*-*- Hypothesis Testing on Imputation Method -*-*-")
        print("Null Hypothesis: The distributions of the data set before and after imputing remain the same.")
        print("Thoughts: Check which column rejects null hypothesis.")
        print("Statistics Test Method: Wilcoxon Test")
        monte_carlo_simulator(data_processed, data_processed_imputed,
                              sample_size=data_processed_imputed.shape[0]//2,
                              iteration=100, test='wilcoxon', confidence=0.05)
        # TODO(sany sanyhew1097618435@163.com): Kruskal Wallis Test - P value - why near 1?
        # print("The statistics test method: Kruskal Wallis Test")
        # monte_carlo_simulator(data_processed, data_processed_imputed, sample_size=50,
        #                       iteration=100, test='kruskal', confidence=0.05)
        probability_plot(data_processed.columns, data_processed, data_processed_imputed)
        basic_info(data_processed_imputed)
        basic_statistic(data_processed_imputed)
        clear_output()
    else:
        data_processed_imputed = data_processed

    # Feature engineering
    # FIXME(hecan sanyhew1097618435@163.com): fix the logic
    logger.debug("Feature Engineering")
    print("The Selected Data Set:")
    show_data_columns(data_processed_imputed.columns)
    fe_flag = 0
    is_feature_engineering = 0
    while True:
        if fe_flag != 1:
            print("Feature Engineering Option:")
            num2option(OPTION)
            is_feature_engineering = limit_num_input(OPTION, SECTION[1], num_input)
            clear_output()
        if is_feature_engineering == 1:
            print("-*-*- Feature Engineering -*-*-")
            feature_built = FeatureConstructor(data_processed_imputed)
            feature_built.index2name()
            feature_built.name_feature()
            feature_built.input_expression()
            feature_built.infix_expr2postfix_expr()
            feature_built.eval_expression()
            clear_output()
            # update the original data with a new feature
            data_processed_imputed = feature_built.create_data_set()
            clear_output()
            basic_info(data_processed_imputed)
            basic_statistic(data_processed_imputed)
            clear_output()
            print("Do you want to continue to construct a new feature?")
            num2option(OPTION)
            fe_flag = limit_num_input(OPTION, SECTION[1], num_input)
            if fe_flag == 1:
                clear_output()
                continue
            else:
                print('Exit Feature Engineering Mode.')
                clear_output()
                break
        else:
            break

    # Mode selection
    logger.debug("Mode Selection")
    print("-*-*- Mode Options -*-*-")
    num2option(MODE_OPTION)
    mode_num = limit_num_input(MODE_OPTION, SECTION[2], num_input)
    clear_output()
    # divide X and y data set when it is supervised learning
    logger.debug("Data Split")
    if mode_num == 1 or mode_num == 2:
        print("-*-*- Data Split -*-*-")
        print("Divide the processing data set into X (feature value) and Y (target value) respectively.")
        # create X data set
        print("Selected sub data set to create X data set:")
        show_data_columns(data_processed_imputed.columns)
        print('The selected X data set:')
        X = create_sub_data_set(data_processed_imputed)
        print('Successfully create X data set.')
        clear_output()
        # create Y data set
        print("Selected sub data set to create Y data set:")
        show_data_columns(data_processed_imputed.columns)
        print('The selected Y data set:')
        y = create_sub_data_set(data_processed_imputed)
        print('Successfully create Y data set.')
        clear_output()
    else:
        # unsupervised learning
        X = data_processed_imputed
        y = None

    # Model option for users
    logger.debug("Model Selection")
    print("-*-*- Model Selection -*-*-:")
    Modes2Models = {1: REGRESSION_MODELS, 2: CLASSIFICATION_MODELS,
                    3: CLUSTERING_MODELS, 4: DECOMPOSITION_MODELS}
    Modes2Initiators = {1: RegressionModelSelection, 2: ClassificationModelSelection,
                        3: ClusteringModelSelection, 4: DecompositionModelSelection}
    MODELS = Modes2Models[mode_num]
    num2option(MODELS)
    all_models_num = len(MODELS) + 1
    # all_models_num = 0
    print(str(all_models_num) + " - All models above to be trained")
    print("Which model do you want to apply?(Enter the Corresponding Number)")
    # FIXME(hecan sanyhew1097618435@163.com): how to train all the algorithms at once
    MODELS.append("all_models")
    model_num = limit_num_input(MODELS, SECTION[2], num_input)
    clear_output()

    # AutoML-training
    is_automl = False
    model = MODELS[model_num - 1]
    if mode_num == 1 or mode_num == 2:
        if model not in NON_AUTOML_MODELS:
            print("Do you want to employ automated machine learning with respect to this algorithm?"
                  "(Enter the Corresponding Number):")
            num2option(OPTION)
            automl_num = limit_num_input(OPTION, SECTION[2], num_input)
            if automl_num == 1:
                is_automl = True
            clear_output()

    # Model trained selection
    logger.debug("Model Training")
    if model_num != all_models_num:
        # run the designated model
        # model = MODELS[model_num - 1]
        run = Modes2Initiators[mode_num](model)
        if not is_automl:
            run.activate(X, y)
        else:
            run.activate(X, y, is_automl)
    else:
        # gain all models result in the specific mode
        for i in range(len(MODELS)):
            run = Modes2Initiators[mode_num](MODELS[i])
            run.activate(X, y)