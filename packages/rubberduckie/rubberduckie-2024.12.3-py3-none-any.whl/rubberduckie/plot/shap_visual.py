import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_categorical_shap(df, shap_values, categorical_feature, pred_class,
                          num_to_plot=10, codes_to_plot=None,
                          plot_type='strip', title=None):
    """Plot Shapley values for categories within categorical feature for the
    purpose of explainability.
    
    Author:
        Justin Trinh @ 2024-06
    
    Args:
        df (DataFrame): DataFrame that was used to generate shap_values
        shap_values (list): Shapley values list of lists generated from explainer
        categorical_feature (str): Categorical feature to be plotted
        pred_class (int): Class for which Shapley values should be extracted from
        num_to_plot (int, optional): Number of categories to plot. Defaults to 10.
        codes_to_plot (iterable, optional): Specific codes for the graph to plot.
            Overwrites default 'Top 10 influential' codes.
        plot_type(str, optional): Options include 'strip' for stripplot, 'swarm'
            for swarmplot, and 'box' for boxplot. Defaults to 'strip'.
    
    Note:
        The plot may take a long time to generate using swarmplot for many
        datapoints.
    """
    
    if pred_class>len(shap_values)-1:
        raise IndexError(f"pred_class is out of range. Largest value is {len(shap_values)-1}")
    
    codes_shap_df = pd.DataFrame({f'{categorical_feature}': df[categorical_feature],
                                   'Shap Values': shap_values[pred_class][:,df.columns.tolist().index(categorical_feature)]})
 
    if codes_to_plot!=None:
        codes_to_show = codes_to_plot
    else:
        codes_to_show = codes_shap_df.groupby(categorical_feature).mean().abs().sort_values(by='Shap Values', ascending=False).iloc[:num_to_plot].index.tolist()
    print(f'Top {num_to_plot} codes of {categorical_feature} by SHAP influence (absolute of mean SHAP value): {codes_to_show}\n')
    
    if df[categorical_feature].dtype not in ['category', 'object']:
        print('*** Note: This function is designed for categorical variables ***')
    
    plot_df = codes_shap_df[codes_shap_df[categorical_feature].isin(codes_to_show)].copy()
    plot_df[categorical_feature] = plot_df[categorical_feature].astype(str)
    
    plt.figure(figsize=(10,10))
    if plot_type=='strip':
        ax = sns.stripplot(plot_df, x='Shap Values', y=str(categorical_feature), order = codes_to_show, jitter=0.3)
    elif plot_type=='swarm':
        ax = sns.swarmplot(plot_df, x='Shap Values', y=str(categorical_feature), order = codes_to_show)
    elif plot_type=='box':
        ax = sns.boxplot(plot_df, x='Shap Values', y=str(categorical_feature), order = codes_to_show)
    else:
        raise ValueError("Invalid plot_type. Possible options are 'strip', 'swarm' or 'box'")
    
    sns.despine(left=True)
    ax.axvline(x=0, linewidth=2, color='orange', ls=':')
    
    if title!=None:
        plt.title(f'{title}\n')
    else:
        plt.title(f'Top {num_to_plot} SHAP Values for {categorical_feature} (Class {pred_class})\n')