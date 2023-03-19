'''
Khalid AlKhalifa, Ciara Malamug, Jasmine Wong
Professor Luo
DS2001 Section 4
Final Project Report: Remodeling in Boston
'''
'''
Problem Statement and Background:
    
The Greater Boston area is home to almost 5 million people across its many
neighborhoods. As one walks through Northeastern's surrounding neighborhoods,
one will immediately see a disparity between the upkeep of residential
propertites. As students in the City of Boston, we wanted to explore the 
differences between neighborhoods through the different impacts of remodeling,
especially as limited research has been done before.


Boston's neighborhoods are quite distinct and have attracted
homeowners to purchase a home in the area, as well as investors to invest in
real estate. With properties across the area increasing in value, we sought to
investigate whether remodeling homes contributes to rising property values.
This analysis would yield key insights for homeowners looking to remodel a 
home in the area, investors seeking to add real estate assets to their
portfolio, as well as lenders giving out loans on investments in real estate.

Question: Which homeowners in the Greater Boston area should remodel their
properties?
'''

'''
Description of Data:
    
This dataset contains data on the assessment of taxable and non-taxable 
property of all types and classifications in the Greater Boston area. The data 
was obtained through Analyze Boston, the City of Boston's open data hub, and 
was quite extensive with 63 columns and 177,091 rows. The relevant columns are
stored in a global list (COLUMNS_OF_INTERST) below.
'''

'''
Methods:
    
We filtered the large dataset to only analyze residential properties, 
categorized in the dataset as R1 (1-family homes), R2 (2-family homes),
R3 (3-family homes) and R4 (4-family homes). We also filtered the data to only 
look at buildings that were constructed in the year 2000 or earlier. We also
decided to calculate building value/sqft of living area to normalize our
analysis across different property types and sizes.

Our mindset for analysis was continuous testing and revision. Therefore we
began by importing all the rows in the columns of interest into a dataframe.
Then, we realized that it was unreasonable to expect newer properties to 
have remodeled recently, so we cut out buildings built after 2000. As we 
calculated value/sqft, we noticed extreme outliers, and refered back to our
original dataset to discover that some living areas were extremely small 
(ex: 1 sqft). Lastly, recognizing that other variables may be creating
outliers, we wrote functions to cut out any remaining outliers.

With the data refined, we calculated summary stats for each land use and each
neighborhood, which we plotted.
'''

'''
Results, Conclusions & Future Work:
    
Our results show that remodeled buildings offer, on average, 
an increase in building value (per square foot of living area) across 
both single-family (R1) and multi-family (R2, R3, R4) properties. The most 
substanial increase in value stems from remodeling single-family homes (R1), 
On average, remodeling four-family homes (R4) leads to the smallest increase
in building value ()

Our results also show that across the Greater Boston Area, remodeling in Boston 
yields the highest average increase in value per square foot in one-family ($259.91),
two-family ($239.41), and three-family homes ($118.75). The cities with the next
highest average increases in value are Roxbury Crossing in single-family homes
($90.90), and Charlestown in two-family ($45.95) and three-family homes ($42.19)
This shows how the difference in remodeling in Boston vs. other neighborhoods 
is quite significant.  
However, in four-family homes, the city with the highest increase in value is
Charlestown at $53.67. 

Stengths:
We started with an expansive dataset provided by the City of Boston, which
ensures the credibility of the data. Despite its size, we were able to
refine our dataset into key components. Using those components, we were able
to create visually appealing graphs that answered our questions in a clear
manner.

Setbacks:
We were able to calculate specific statistics, however, due to the broad
nature of certain column headers, we can only be left to speculate about the 
underlying causes behind the increases in value. Additionally, some of the
data points were unclear. For example, multiple living areas were listed as 
1 sqft, indicated that the City may lack data on specific properties.
Furthermore, there is a ldata on remodeling specifics.

Future studies:
For future studies, we could further analyze the distinctions between different 
neighborhoods (ex: ratio of remodeled to unremodeled homes, number of 
properties in neighborhood). We could also utilize market values (instead of 
building values) for all properties to gain a more accuarate measure of the 
current value of the property. We could better assess the return on investment
on these properties by investigating how taxes contribute to overall expenses.
Additionally, we can compare the investment opportunity in the City of Boston,
the city with the greatest increase in building value in R1, R2 & R3 
properties, with other metropolitan cities such as New York City, Austin, and 
Charlotte.
'''

#import libraries
import pandas as pd
import matplotlib.pyplot as plt

#define global for relevant column headers for creating df
COLUMNS_OF_INTEREST = ["CITY", "LU", "LIVING_AREA", "BLDG_VALUE", "YR_BUILT",
                       "YR_REMODEL", "ZIPCODE"]   

#define global for neighborhoods for splitting df    
CITY_LIST = ["ALLSTON", "BOSTON", "BRIGHTON", "BROOKLINE", "CHARLESTOWN", 
             "CHESNUT HILL", "DEDHAM", "DORCHESTER", "EAST BOSTON",
             "HYDE PARK", "JAMAICA PLAIN", "MATTAPAN", "ROSLINDALE","ROXBURY", 
             "ROXBURY CROSSIN", "SOUTH BOSTON", "WEST ROXBURY"]

#define color dictionary for neighborhood graphs
COLOR_DICT = {"ALLSTON" : "sandybrown", "BOSTON" : "seagreen", 
              "BRIGHTON" : "lightseagreen", "BROOKLINE" : "silver", 
              "CHARLESTOWN" : "steelblue", "CHESNUT HILL" : "beige", 
              "DEDHAM" : "oldlace", "DORCHESTER" : "cadetblue",
              "EAST BOSTON" : "darkorchid", "HYDE PARK" : "lawngreen", 
              "JAMAICA PLAIN" : "khaki", "MATTAPAN" : "forestgreen", 
              "ROSLINDALE" : "salmon","ROXBURY" : "sienna", 
              "ROXBURY CROSSIN" : "firebrick", 
              "SOUTH BOSTON" : "palevioletred",
              "WEST ROXBURY" : "rebeccapurple"}

#data file
REAL_ESTATE_FILE = "boston_real_estate_data.csv"

def read_csv(filename):
    '''
    reads in csv file using pandas and return relvant columns in dataframe

    Parameters
    ----------
    filename : str
        name of file we are reading in

    Returns
    -------
    df (dataframe): the dataframe from the file that we want to analyze

    '''
    #create df variable to store pandas df
    real_estate_df = pd.read_csv(filename)
    
    # Uses a global variable to return only the columns we're interested in 
    real_estate_df = real_estate_df[COLUMNS_OF_INTEREST]
    
    return real_estate_df

def remove_symbols(df):
    """
    Removes the "$" and "," chars that makes it hard to analyze the data

    Parameters
    ----------
    df : dataframe
        dataframe that we're analyzing.

    Returns
    -------
    df : dataframe
        Edited dataframe.

    """
    #overwrites df with removed symbols
    df["BLDG_VALUE"] = df["BLDG_VALUE"].str.replace("$", '')
    df["BLDG_VALUE"] = df["BLDG_VALUE"].str.replace(",", '')
    
    return df

def sep_by_yr_built(df):
    """
    Separates given dataframe into another dataframe based on buildings that 
    were built before the turn of the century (Yr: 2000)

    Parameters
    ----------
    df : dataframe
        dataframe that we're analyzing.

    Returns
    -------
    old_prop_df : dataframe
        All properties that were in the dataframe and built before the year
        2000.

    """
    # If the year built is less then 2000, those values are part of the new
    # dataframe
    #unreasonable to expect remodeling for younger buildings < 21 years old
    old_prop_df = df[df.YR_BUILT < 2000]
    
    return old_prop_df

def cut_la_outliers(df):
    """
    Gets rid of any "weird living area(la) data." In this case, we were
    getting values for the living area with 1 sqft. This accounted for
    anything less than 100 sqft in that category

    Parameters
    ----------
    df : dataframe
        dataframe that we're analyzing.

    Returns
    -------
    cut_outliers_df : df
        Returns the dataframe without the living area outliers.

    """
    # Keeps tha values where the living area is greater than 100 sqft
    cut_outliers_df = df[df.LIVING_AREA > 100]
    
    return cut_outliers_df

def sep_by_lu(df):
    '''
    separates data frame into 4 data frames depending on land use 
    R1 = residential 1-family
    R2 = residential 2-family
    R3 = residential 3-family
    R4 = residential 4 or more family

    Parameters
    ----------
    df : dataframe
        general df of interest

    Returns
    -------
    r1_prop_df : df
        df containing data about residential 1-family properties in Boston
    r2_prop_df : df
        df containing data about residential 2-family properties in Boston
    r3_prop_df : df
        df containing data about residential 3-family properties in Boston
    r4_prop_df : df
        df containing data about residential 4 or more family properties
        in Boston

    '''
    # Creates dataframes for the R1, R2, R3, and R4 properties
    r1_prop_df = df[df["LU"] == "R1"]
    r2_prop_df = df[df["LU"] == "R2"]
    r3_prop_df = df[df["LU"] == "R3"]
    r4_prop_df = df[df["LU"] == "R4"]
    
    return r1_prop_df, r2_prop_df, r3_prop_df, r4_prop_df

def val_per_sqft(df):
    """
    Calculates and creates a new column containing the building value per 
    square foot of living area

    Parameters
    ----------
    df : datafrane
        The dataframe we're interested in.

    Returns
    -------
    df : dataframe
        The same dataframe with a value per sqft column.

    """
    df['VAL/SQFT'] = df["BLDG_VALUE"].astype("float64") \
                        / df["LIVING_AREA"].astype("float64") 
    
    return df
    
def split_remod(df):
    """
    Splits the dataframe into two. One for the buildings that were remodeled
    and one for the ones that weren't

    Parameters
    ----------
    df : dataframe
        The dataframe that we're interested in.

    Returns
    -------
    remod_df : dataframe
        The dataframe containing the remodeled buildings.
    unremod_df : dataframe
        The dataframe contining the unremodeled buildings.

    """
    # If the YR_REMODEL column is not blank, the building was remodeled
    remod_df = df[df.YR_REMODEL.notnull()]
    # If the YR_REMODEL column is blank, the building wasn't remodeled
    unremod_df = df[df.YR_REMODEL.isnull()]
    
    return remod_df, unremod_df

def val_per_sqft_stats(remod_df, unremod_df):
    """
    Returns the summary stats of the VAL/SQFT column for remod and
    unremod df's

    Parameters
    ----------
    remod_df : dataframe
        A dataframe containing the remodeled data.
    unremod_df : dataframe
        A dataframe containing the unremodeled data.

    Returns
    -------
    remod_stats : series
        A series containing the remodeled statistics.
    unremod_stats : series
        A series containing the unremodeled statitsics.

    """
    remod_stats = remod_df["VAL/SQFT"].describe()
    unremod_stats = unremod_df["VAL/SQFT"].describe()

    return remod_stats, unremod_stats


def compare_lu_remod(stats1, stats2, stats3, stats4):
    """
    Takes in the four stats and plots the comparison by the means of the 
    remodeled and unremodeled data from each of the living uses

    Parameters
    ----------
    stats1 : tuple
        R1 remodled and unremodeled stats.
    stats2 : tuple
        R2 remodled and unremodeled stats.
    stats3 : tuple
        R3 remodled and unremodeled stats.
    stats4 : tuple
        R4 remodled and unremodeled stats.

    Returns
    -------
    None. Plots a graph.

    """
    #establish a color patter to distinguish remod vs unremod
    color_pattern = ["slateblue", "turquoise"]
    
    # The 0th element of the stat tuple is the remodeled data and the 1st 
    # element is the unremodeled data
    y = [stats1[0]["mean"], stats1[1]["mean"], 
         stats2[0]["mean"], stats2[1]["mean"], 
         stats3[0]["mean"], stats3[1]["mean"], 
         stats4[0]["mean"], stats4[1]["mean"]]
    
    # Positioning of the bar graphs to create space between diff LU
    x_pos = [1,2,4,5,7,8,10,11]
    plt.bar(x_pos, y, color = color_pattern * 4)
    
def calc_nbhd_stats(remod_df, unremod_df):
    """
    Calculates the neighborhood average and returns lists containing them for
    remodeled and unremodled data.

    Parameters
    ----------
    remod_df : dataframe
        A dataframe containing the remodeled data.
    unremod_df : dataframe
        A dataframe containing the unremodeled data.

    Returns
    -------
    remod_stats_list : list
        A list containing the stats for each remodeled house in each
        neighborhood.
    unremod_stats_list : list
        A list contining the stats for each unremodeled house in each
        neighborhood.

    """
    #create empty lists to store stats
    remod_stats_list = []
    unremod_stats_list = []
    
    #iterate through each neighborhood in global and append nbhd stats
    #in remod and unremod lists
    for city in CITY_LIST:
        remod_stats = remod_df[remod_df.CITY == city]["VAL/SQFT"].describe()
        
        unremod_stats = unremod_df[unremod_df.CITY == city]["VAL/SQFT"] \
                                                            .describe()
        
        remod_stats_list.append(remod_stats)
        unremod_stats_list.append(unremod_stats)
    
    return remod_stats_list, unremod_stats_list

def has_outlier(stats):
    """
    when given summary stats, returns TRUE if stats contain outlier
    FALSE when no outlier

    Parameters
    ----------
    stats : TYPE
        DESCRIPTION.

    Returns
    -------
    boolean
        TRUE = outlier, FALSE = no outlier

    """
    # There are no outliers if
    # Q3 + IQR * 1.5  > max or Q1 - IQR * 1.5 < min
    #upper bound > max, lower bound < min
    return (stats[6] + ((stats[6] - stats[4]) * 1.5) < stats[7]) \
            or (stats[4] - ((stats[6] - stats[4]) * 1.5) > stats[3])

def return_bounds(stats):
    """
    when given summary stats, calcs and returns the upper and lower bounds
    for outliers

    Parameters
    ----------
    stats : series
        series contianing summary statistics for each neighborhood

    Returns
    -------
    upper_bound : float
        upper bound for outliers
    lower_bound : floar
        lower bound for outliers

    """
    #upper bound = Q3 + (IQR * 1.5)
    upper_bound = stats[6] + ((stats[6] - stats[4]) * 1.5)
    #lower bound = Q1 - (IQR * 1.5)
    lower_bound = stats[4] - ((stats[6] - stats[4]) * 1.5)
                        
    return upper_bound, lower_bound
            
def outlier_cutoff(remod_stats_list, unremod_stats_list):
    """
    when given lists of unremod and remod stats, calculates the bounds
    and returns a remod and unremod list containing each nbhd's outlier bounds

    Parameters
    ----------
    remod_stats_list : list
        list of summary stats in series for each neighborhood (remod)
    unremod_stats_list : list
        list of summary stats in series for each neighborhood (unremod)

    Returns
    -------
    remod_cutoff : list
        list of tuples (upper bound, lower bound) for each nbhd
    unremod_cutoff : list
        list of tuples (upper bound, lower bound) for each nbhd

    """
    #create empty list to store cutoffs
    remod_cutoff = []
    unremod_cutoff = []
    
    #iterates through nbhd indices and appends bounds for each nbhd to proper
    #list
    for i in range(len(CITY_LIST)):
        remod_cutoff.append(return_bounds(remod_stats_list[i]))
        unremod_cutoff.append(return_bounds(unremod_stats_list[i]))
        
    return remod_cutoff, unremod_cutoff

def cut_outliers(remod_df, unremod_df, out_bound):
    """
    when given remod and unremod df's and bound cutoffs, removes data ouside
    of outlier bounds and returns updated df's w/o outliers

    Parameters
    ----------
    remod_df : df
        df containg remod properties
    unremod_df : df
        df containing unremod properties
    out_bound : tuple
        tuple (remod bounds (upper bound, lower bound), 
               unremod bounds (upper bound, lower bound))
        
    Returns
    -------
    new_remod_df : df
        remod df without outliers
    new_unremod_df : df
        unremod df without outliers

    """
    #create empty dataframe to populate with non-outlier data
    new_remod_df = pd.DataFrame()
    new_unremod_df = pd.DataFrame()
    
    #iterate through neighborhood indices
    for i in range(len(CITY_LIST)):
        # For each neighborhood only retains the values less than the upper 
        # bound and greater than the lower bound for outliers
        nbhd_remod_df = remod_df[remod_df.CITY == CITY_LIST[i]]
        
        # out_bound[0][i][0/1]
        # 0 for remod
        # i for neighborhood
        # 0/1 for upper bound/lower bound
        nbhd_remod_df = nbhd_remod_df[nbhd_remod_df["VAL/SQFT"] 
                                      < out_bound[0][i][0]]
        nbhd_remod_df = nbhd_remod_df[nbhd_remod_df["VAL/SQFT"] 
                                      > out_bound[0][i][1]]
        
        # Appends the new dataframe to the placeholder
        new_remod_df = new_remod_df.append(nbhd_remod_df)
        
        # For each neighborhood only retains the values less than the upper 
        # bound and greater than the lower bound for outliers
        nbhd_unremod_df = unremod_df[unremod_df.CITY == CITY_LIST[i]]
        
        # out_bound[1][i][0/1]
        # 1 for unremod
        # i for neighborhood
        # 0/1 for upper bound/lower bound
        nbhd_unremod_df = nbhd_unremod_df[nbhd_unremod_df["VAL/SQFT"] 
                                          < out_bound[1][i][0]]
        nbhd_unremod_df = nbhd_unremod_df[nbhd_unremod_df["VAL/SQFT"] 
                                          > out_bound[1][i][1]]
        
        # Appends the new dataframe to the placeholder
        new_unremod_df = new_unremod_df.append(nbhd_unremod_df)
        
    return new_remod_df, new_unremod_df
            
def calc_diff(lu_tuple):
    """
    Calculate the average difference between the means of remod and 
    unremod houses in each neighborhood

    Parameters
    ----------
    lu_tuple : tuple
        A tuple containing the remod and unremod data. Within those are
        the stats for each neighborhood. (remod stats, unremod stats)

    Returns
    -------
    nbhd_diff_list : list
        A list containing the differences between the means for remodled and
        unremodled data (remod - unremod) for each neighborhood. 

    """
    #create an empty list to store differences
    nbhd_diff_list = []
    
    #iterate through indices for nbhd
    for i in range(len(CITY_LIST)):
        # [0 or 1 for remodled or unremodled][neighborhood][1 for the mean]
        #calc difference by remod mean - unremod mean
        diff = lu_tuple[0][i][1] - lu_tuple[1][i][1]
        #append difference to diff list
        nbhd_diff_list.append(diff)
        
    return nbhd_diff_list

def means_to_nbhd(means_list):
    """
    Creates and returns a dictionary mapping the difference of means to the
    neighborhood

    Parameters
    ----------
    means_list : list
        A list containing remod/unremod mean differences as floats.
        Has the same length as the CITY_LIST

    Returns
    -------
    means_nbhd_dict : dict
        Associates the means differences to a neighborhood. (mean: nbhd)

    """
    #create empty dict
    means_nbhd_dict = {}
    
    #iterate through nbhd indices
    for i in range(len(means_list)):
        #creates key, value in form of (mean: nbhd)
        means_nbhd_dict[means_list[i]] = CITY_LIST[i]
        
    return means_nbhd_dict
    

def sort_by_greatest(nbhd_diff_list):
    """
    when given list of diffs, finds the top 5 differences and returns them
    in a list

    Parameters
    ----------
    nbhd_diff_list : list
        A list containing all of the diff of means btw remod and unremod.

    Returns
    -------
    nbhd_sorted_diff : list
        A list containing the top 5 nbhd diff of means.

    """
    #create an empty list to store sorted differemces of means
    nbhd_sorted_diff_list = []
    
    #iterate through nbhd diff mean lst
    for num in nbhd_diff_list:
        
        #append diff mean if not blank
        if not pd.isna(num):
            nbhd_sorted_diff_list.append(num)
    
    #sort list from least to greatest
    nbhd_sorted_diff_list.sort()
    
    #reverse list to have greatest to least
    nbhd_sorted_diff_list.reverse()

    #extract first 5 elements for top5 diff list
    top5_diff = nbhd_sorted_diff_list[:5]
    
    return top5_diff

def plot_top_nbhd(nbhd_dict, top5_diff):
    """
    Plots the top 5 neighborhoods 

    Parameters
    ----------
    nbhd_dict : dict
        A dictionary mapping the diff of means to the neighborhood.
    top5_diff : list
        A list containing the top 5 mean differences.

    Returns
    -------
    None. Plots a graph

    """
    #iterate through top 5 diff list
    for mean in top5_diff:
        #plot with nbhd (value) as x, nbhd mean (key) as y
        plt.bar(nbhd_dict[mean], mean, color = COLOR_DICT[nbhd_dict[mean]])
    
if __name__ == "__main__":
    
    # Reads in the file and formats the data in a way that's easy for us to 
    # analyze (create df, remove symbols, cut out young props, cut out 
    #unreasonably tiny liv areas)
    real_estate_df = read_csv(REAL_ESTATE_FILE)
    real_estate_df = remove_symbols(real_estate_df)
    old_prop_df = sep_by_yr_built(real_estate_df)
    cut_la_outliers_df = cut_la_outliers(old_prop_df)
    
    # Separates the data into the 4 living uses we're focusing on 
    r1_prop_df, r2_prop_df, r3_prop_df, r4_prop_df = \
                                            sep_by_lu(cut_la_outliers_df)
    
    # Calculates and adds the value per square foot column to the dataframes
    r1_prop_df = val_per_sqft(r1_prop_df)
    r2_prop_df = val_per_sqft(r2_prop_df)
    r3_prop_df = val_per_sqft(r3_prop_df)
    r4_prop_df = val_per_sqft(r4_prop_df)
    
    # Splits the land uses into remodeled and unremodeled df's
    r1_remod_df, r1_unremod_df = split_remod(r1_prop_df)
    r2_remod_df, r2_unremod_df = split_remod(r2_prop_df)
    r3_remod_df, r3_unremod_df = split_remod(r3_prop_df)
    r4_remod_df, r4_unremod_df = split_remod(r4_prop_df)
    
    # calcs and stores the summary stats of the VAL/SQFT column per land use 
    r1_stats = val_per_sqft_stats(r1_remod_df, r1_unremod_df)
    r2_stats = val_per_sqft_stats(r2_remod_df, r2_unremod_df)
    r3_stats = val_per_sqft_stats(r3_remod_df, r3_unremod_df)
    r4_stats = val_per_sqft_stats(r4_remod_df, r4_unremod_df)
    
    # Calcs and stores the summary statistics per neighborhood
    r1_nbhd_stats = calc_nbhd_stats(r1_remod_df, r1_unremod_df)
    r2_nbhd_stats = calc_nbhd_stats(r2_remod_df, r2_unremod_df)
    r3_nbhd_stats = calc_nbhd_stats(r3_remod_df, r3_unremod_df)
    r4_nbhd_stats = calc_nbhd_stats(r4_remod_df, r4_unremod_df)
    
    # indentifies the outlier bounds and cuts out the outliers
    r1_out_bounds = outlier_cutoff(r1_nbhd_stats[0], r1_nbhd_stats[1])
    r1_remod_df, r1_unremod_df = cut_outliers(r1_remod_df, r1_unremod_df,
                                              r1_out_bounds)
    
    r2_out_bounds = outlier_cutoff(r2_nbhd_stats[0], r2_nbhd_stats[1])
    r2_remod_df, r2_unremod_df = cut_outliers(r2_remod_df, r2_unremod_df,
                                              r2_out_bounds)
    
    r3_out_bounds = outlier_cutoff(r3_nbhd_stats[0], r3_nbhd_stats[1])
    r3_remod_df, r3_unremod_df = cut_outliers(r3_remod_df, r3_unremod_df,
                                              r3_out_bounds)
    
    r4_out_bounds = outlier_cutoff(r4_nbhd_stats[0], r4_nbhd_stats[1])
    r4_remod_df, r4_unremod_df = cut_outliers(r4_remod_df, r4_unremod_df,
                                              r4_out_bounds)
    
    # Recalculates the stats of the VAL/SQFT column after removing outliers
    #per land use
    r1_stats = val_per_sqft_stats(r1_remod_df, r1_unremod_df)
    r2_stats = val_per_sqft_stats(r2_remod_df, r2_unremod_df)
    r3_stats = val_per_sqft_stats(r3_remod_df, r3_unremod_df)
    r4_stats = val_per_sqft_stats(r4_remod_df, r4_unremod_df)
    
    # Recalculates the statistics per neighborhood after removing outliers
    r1_nbhd_stats = calc_nbhd_stats(r1_remod_df, r1_unremod_df)
    r2_nbhd_stats = calc_nbhd_stats(r2_remod_df, r2_unremod_df)
    r3_nbhd_stats = calc_nbhd_stats(r3_remod_df, r3_unremod_df)
    r4_nbhd_stats = calc_nbhd_stats(r4_remod_df, r4_unremod_df)
    
    # Calculates the difference in means between the remodeled and unremodeled
    #data for each land use
    r1_nbhd_diff_list = calc_diff(r1_nbhd_stats)
    r2_nbhd_diff_list = calc_diff(r2_nbhd_stats)
    r3_nbhd_diff_list = calc_diff(r3_nbhd_stats)
    r4_nbhd_diff_list = calc_diff(r4_nbhd_stats)
    
    # Creates a dictionary associating the mean to the neighnorhood, makes it 
    # easier to plot
    r1_nbhd_dict = means_to_nbhd(r1_nbhd_diff_list)
    r2_nbhd_dict = means_to_nbhd(r2_nbhd_diff_list)
    r3_nbhd_dict = means_to_nbhd(r3_nbhd_diff_list)
    r4_nbhd_dict = means_to_nbhd(r4_nbhd_diff_list)
    
    # Sorts and returns the top 5 nbhds with the greatest differences of means
    r1_top5_diff = sort_by_greatest(r1_nbhd_diff_list)
    r2_top5_diff = sort_by_greatest(r2_nbhd_diff_list)
    r3_top5_diff = sort_by_greatest(r3_nbhd_diff_list)
    r4_top5_diff = sort_by_greatest(r4_nbhd_diff_list)
    
    # Create figure 1: Remodeled and Unremodeled Averages for Land Uses
    plt.figure(1, figsize = (12,10))
    
    compare_lu_remod(r1_stats, r2_stats, r3_stats, r4_stats)
    plt.xticks([1,2,4,5,7,8,10,11], 
               labels=["R1 Remodeled", "R1 Unremodeled", "R2 Remodeled", 
                       "R2 Unremodeled", "R3 Remodeled", "R3 Unremodeled", 
                       "R4 Remodeled", "R4 Unremodeled"],
               rotation=90)
    plt.ylabel("Mean Value Per Sqft of Living Area ($)")
    plt.title("Comparison of Mean Building Value Per Sqft of Living Area")
    
    plt.savefig("compare_fam_graph", bbox_inches = "tight")
    
    # Plots the top 5 nbhd differences of mean for R1, customize graph
    plt.figure(2, figsize = (12,10))
    
    plot_top_nbhd(r1_nbhd_dict, r1_top5_diff)
    plt.xticks(rotation = 90)
    plt.ylabel("Average Increase in Value/Sqft")
    plt.title("Top Average Increase in Value/Sqft in Remodeled vs"
              + " Unremodeled 1-Fam Homes")
    plt.rc('font', size= 18)  
    
    plt.savefig("1_fam_graph", bbox_inches = "tight")
    
    # Plots the top 5 nbhd differences of mean for R2, customize graph
    plt.figure(3, figsize = (10,8))
    
    plot_top_nbhd(r2_nbhd_dict, r2_top5_diff)
    plt.xticks(rotation = 90)
    plt.ylabel("Average Increase in Value/Sqft")
    plt.title("Top Average Increase in Value/Sqft in Remodeled vs Unremodeled"
              + " 2-Fam Homes")
    
    plt.savefig("2_fam_graph", bbox_inches = "tight")
    
    # Plots the top 5 nbhd differences of mean for R3, customize graph
    plt.figure(4, figsize = (10,8))
    
    plot_top_nbhd(r3_nbhd_dict, r3_top5_diff)
    plt.xticks(rotation = 90)
    plt.ylabel("Average Increase in Value/Sqft")
    plt.title("Top Average Increase in Value/Sqft in Remodeled vs Unremodeled"
              + " 3-Fam Homes")
    
    plt.savefig("3_fam_graph", bbox_inches = "tight")
    
    # Plots the top 5 nbhd differences of mean for R4, customize graph
    plt.figure(5, figsize = (10,8))
    
    plot_top_nbhd(r4_nbhd_dict, r4_top5_diff)
    plt.xticks(rotation = 90)
    plt.ylabel("Average Increase in Value/Sqft")
    plt.title("Top Average Increase in Value/Sqft in Remodeled vs Unremodeled"
              + " 4-Fam Homes")
    
    plt.savefig("4_fam_graph", bbox_inches = "tight")
    