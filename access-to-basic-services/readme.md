# Share of the population with access to basic services - Data package

This data package contains the data that powers the chart ["Share of the population with access to basic services"](https://ourworldindata.org/grapher/access-to-basic-services?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For most countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The remaining columns are the data columns, each of which is a time series. If the CSV data is downloaded using the "full data" option, then each column corresponds to one time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data columns are transformed depending on the chart type and thus the association with the time series might not be as straightforward.


## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

### How we process data at Our World In Data
All data and visualizations on Our World in Data rely on data sourced from one or several original data providers. Preparing this original data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
[Read about our data pipeline](https://docs.owid.io/projects/etl/)

## Detailed information about each time series


## Share of the population with access to electricity – World Bank
Access to electricity means having an electricity source that can provide very basic lighting, and charge a phone or power a radio for 4 hours per day.
Last updated: February 27, 2026  
Next update: February 2027  
Date range: 1990–2023  
Unit: % of population  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Data compiled from multiple sources by the World Bank – with minor processing by Our World in Data

#### Full citation
Data compiled from multiple sources by the World Bank – with minor processing by Our World in Data. “Share of the population with access to electricity – World Bank” [dataset]. SDG 7.1.1 Electrification Dataset, World Bank, via World Bank, “World Development Indicators 125” [original data].
Source: Data compiled from multiple sources by the World Bank – with minor processing by Our World In Data

### What you should know about this data
* Access to electricity improves people's living conditions in many ways. [Light at night](https://ourworldindata.org/light-at-night) makes it possible to get together after sunset; mobile phones allow us to stay in touch with those far away; refrigeration reduces food waste; and household appliances free up time from chores.
* This data captures whether people have access to the most basic electricity supply — just enough to provide basic lighting and charge a phone or power a radio for 4 hours per day.
* It shows that, especially in several African countries, a large share of the population lacks the benefits of basic electricity.
* Universal access to electricity by 2030 is one of the United Nations [Sustainable Development Goals](https://ourworldindata.org/sdgs/affordable-clean-energy#sdg-indicator-7-1-1-access-to-electricity).
* This data comes from the World Bank's World Development Indicators. Estimates are based on national household surveys, census data, and reports from energy providers or government agencies. Where data is missing, values are estimated by the source using a model based on trends across countries, regions, and time. Countries classified as “developed” by the United Nations are assumed to have universal access.
* To learn more, read our article: [Definitions: access to electricity](https://ourworldindata.org/definition-electricity-access).

### How is this data described by its producer - Data compiled from multiple sources by the World Bank?
Access to electricity is the percentage of population with access to electricity. Electrification data are collected from industry, national surveys and international sources.

### Aggregation method:
Population-weighted average

### Statistical concept and methodology:
Methodology: The World Bank’s Global Electrification Database (GED) compiles nationally representative household survey data, and occasionally census data, from sources going back as far as 1990. The database also incorporates data from the Socio-Economic Database for Latin America and the Caribbean (SEDLAC), Middle East and North Africa Poverty Database (MNAPOV) and the Europe and Central Asia Poverty Database (ECAPOV), which are based on similar surveys. At the time of this analysis, the GED contained 1,375 surveys for 149 countries in 1990-2021.

### Development relevance:
Maintaining reliable and secure electricity services while seeking to rapidly decarbonize power systems is a key challenge for countries throughout the world. More and more countries are becoming increasing dependent on reliable and secure electricity supplies to underpin economic growth and community prosperity. This reliance is set to grow as more efficient and less carbon intensive forms of power are developed and deployed to help decarbonize economies.



















Energy is necessary for creating the conditions for economic growth. It is impossible to operate a factory, run a shop, grow crops or deliver goods to consumers without using some form of energy. Access to electricity is particularly crucial to human development as electricity is, in practice, indispensable for certain basic activities, such as lighting, refrigeration and the running of household appliances, and cannot easily be replaced by other forms of energy. Individuals' access to electricity is one of the most clear and un-distorted indication of a country's energy poverty status.



















Electricity access is increasingly at the forefront of governments' preoccupations, especially in the developing countries. As a consequence, a lot of rural electrification programs and national electrification agencies have been created in these countries to monitor more accurately the needs and the status of rural development and electrification.



















Use of energy is important in improving people's standard of living. But electricity generation also can damage the environment. Whether such damage occurs depends largely on how electricity is generated. For example, burning coal releases twice as much carbon dioxide - a major contributor to global warming - as does burning an equivalent amount of natural gas.

### Source

#### SDG 7.1.1 Electrification Dataset, World Bank, via World Bank – World Development Indicators
Retrieved on: 2026-02-27  
Retrieved from: https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS  


## Share of the population with access to clean fuels for cooking – World Bank
Access to [clean fuels or technologies](#dod:clean-cooking-fuels) such as natural gas, electricity, and clean cookstoves reduces exposure to indoor air pollutants, a leading cause of death in low-income households.
Last updated: February 27, 2026  
Next update: February 2027  
Date range: 2000–2023  
Unit: % of population  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
World Health Organization (via World Bank) – with minor processing by Our World in Data

#### Full citation
World Health Organization (via World Bank) – with minor processing by Our World in Data. “Share of the population with access to clean fuels for cooking – World Bank” [dataset]. Tracking SDG 7: The Energy Progress Report, via World Bank, “World Development Indicators 125” [original data].
Source: World Health Organization (via World Bank) – with minor processing by Our World In Data

### How is this data described by its producer - World Health Organization (via World Bank)?
Access to clean fuels and technologies for cooking is the proportion of total population primarily using clean cooking fuels and technologies for cooking. Under WHO guidelines, kerosene is excluded from clean cooking fuels.

Statistical concept and methodology: Data for access to clean fuels and technologies for cooking are based on the World Health Organization's (WHO) Global Household Energy Database. They are collected among different sources: only data from nationally representative household surveys (including national censuses) were used. Survey sources include Demographic and Health Surveys (DHS) and Living Standards Measurement Surveys (LSMS), Multi-Indicator Cluster Surveys (MICS), the World Health Survey (WHS), other nationally developed and implemented surveys, and various government agencies (for example, ministries of energy and utilities).

Trends in the proportion of the population using each fuel type are estimated using a single multivariate hierarchical model, with urban and rural disaggregation. Estimates for overall "polluting" fuels (unprocessed biomass, charcoal, coal, and kerosene) and "clean" fuels (gaseous fuels, electricity, as well as an aggregation of any other clean fuels like alcohol) are produced by aggregating estimates of relevant fuel types. The model was used to derive clean fuel use estimates for 191 countries (ref. Stoner, O., Shaddick, G., Economou, T., Gumy, S., Lewis, J., Lucio, I., Ruggeri, G. and Adair-Rohani, H. (2020), Global household energy model: a multivariate hierarchical approach to estimating trends in the use of polluting and clean fuels for cooking. J. R. Stat. Soc. C, 69: 815-839). Countries classified by the World Bank as high income (57 countries) in the 2022 fiscal year are assumed to have universal access to clean fuels and technologies for cooking.

### Source

#### Tracking SDG 7: The Energy Progress Report, via World Bank – World Development Indicators
Retrieved on: 2026-02-27  
Retrieved from: https://data.worldbank.org/indicator/EG.CFT.ACCS.ZS  


## Improved water source
Last updated: February 27, 2026  
Next update: February 2027  
Date range: 2000–2024  
Unit: % of population  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026) – processed by Our World in Data

#### Full citation
WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026) – processed by Our World in Data. “Improved water source” [dataset]. WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank, “World Development Indicators 125” [original data].
Source: WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026) – processed by Our World In Data

### How is this data described by its producer - WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026)?
The percentage of people using at least basic water services. This indicator encompasses both people using basic water services as well as those using safely managed water services. Basic drinking water services is defined as drinking water from an improved source, provided collection time is not more than 30 minutes for a round trip. Improved water sources include piped water, boreholes or tubewells, protected dug wells, protected springs, and packaged or delivered water.

### Aggregation method:
Weighted average

### Statistical concept and methodology:
Methodology: The data sources for drinking water services are household surveys such as Demographic and Health Surveys (DHS) and Multiple Indicator Cluster Surveys (MICS), administrative data, census, and other datasets such as compilations by international or regional initiatives (e.g., IB-NET) or studies conducted by research institutions. Based on these national datasets, JMP estimates the proportion of the people accessing different levels of services by using linear regression. You can find the details of estimates including the rules on interpolation, extrapolation and extension in the JMP’s methodology report (https://washdata.org/reports/jmp-2017-methodology).
Statistical concept(s): The JMP classifies the sanitation service levels into five tiers, ranging from the most to the least favorable: safely managed, basic, limited, unimproved, and surface water (Reference: https://washdata.org/monitoring/drinking-water). This indicator encompasses both people using basic water services as well as those using safely managed water services.

### Development relevance:
Water is considered to be the most important resource for sustaining ecosystems, which provide life-supporting services for people, animals, and plants. Global access to safe water and proper hygiene education can reduce illness and death from disease, leading to improved health, poverty reduction, and socio-economic development. However, many countries are challenged to provide these basic necessities to their populations, leaving people at risk for water, sanitation, and hygiene (WASH)-related diseases. Because contaminated water is a major cause of illness and death, water quality is a determining factor in human poverty, education, and economic opportunities.





















Lack of access to adequate drinking water services contributes to deaths and illness, especially in children. Water based disease transmission by drinking contaminated water is responsible for significant outbreaks of diseases such as cholera and typhoid and includes diarrheal diseases, viral hepatitis A, cholera, dysentery and dracunculiasis (Guineaworm disease). Improving access to clean drinking water is a crucial element in the reduction of under-five mortality and morbidity and there is evidence that ensuring higher levels of drinking water services has a greater impact.





















Women and children spend millions of hours each year fetching water. The chore diverts their time from other important activities (for example attending school, caring for children, participating in the economy). When water is not available on premises and has to be collected, women and girls are almost two and a half times more likely than men and boys to be the main water carriers for their families.





















Many international organizations use access to safe drinking water and hygienic sanitation facilities as a measure for progress in the fight against poverty, disease, and death. Access to safe drinking water is also considered to be a human right, not a privilege, for every man, woman, and child. Economic benefits of safe drinking water services include higher economic productivity, more education, and health-care savings.

### Limitations and exceptions:
National, regional and income group estimates are made when data are available for at least 50 percent of the population.

### Source

#### WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank – World Development Indicators
Retrieved on: 2026-02-27  
Retrieved from: https://data.worldbank.org/indicator/SH.H2O.BASW.ZS  


## Improved sanitation facilities
Last updated: February 27, 2026  
Next update: February 2027  
Date range: 2000–2024  
Unit: % of population  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026) – processed by Our World in Data

#### Full citation
WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026) – processed by Our World in Data. “Improved sanitation facilities” [dataset]. WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank, “World Development Indicators 125” [original data].
Source: WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026) – processed by Our World In Data

### How is this data described by its producer - WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank (2026)?
The percentage of people using at least basic sanitation services, that is, improved sanitation facilities that are not shared with other households. This indicator encompasses both people using basic sanitation services as well as those using safely managed sanitation services. Improved sanitation facilities include flush/pour flush to piped sewer systems, septic tanks or pit latrines; ventilated improved pit latrines, compositing toilets or pit latrines with slabs.

### Aggregation method:
Weighted average

### Statistical concept and methodology:
Methodology: The data sources for sanitation services are household surveys such as Demographic and Health Surveys (DHS) and Multiple Indicator Cluster Surveys (MICS), administrative data, census, and other datasets such as compilations by international or regional initiatives (e.g., IB-NET) or studies conducted by research institutions. Based on these national datasets, JMP estimates the proportion of the people accessing different levels of services by using linear regression. You can find the details of estimates including the rules on interpolation, extrapolation and extension in the JMP’s methodology report (https://washdata.org/reports/jmp-2017-methodology).
Statistical concept(s): The JMP classifies the sanitation service levels into five tiers, ranging from the most to the least favorable: safely managed, basic, limited, unimproved, and open defecation (Reference: https://washdata.org/monitoring/sanitation). This indicator encompasses both people using basic sanitation services as well as those using safely managed sanitation services.

### Development relevance:
Sanitation is fundamental to human development. Many international organizations use hygienic sanitation facilities as a measure for progress in the fight against poverty, disease, and death. Access to proper sanitation is also considered to be a human right, not a privilege, for every man, woman, and child.





















Sanitation generally refers to the provision of facilities and services for the safe disposal of human urine and feces. Inadequate sanitation is a major cause of disease world-wide and improving sanitation is known to have a significant beneficial impact on people's health. Basic and safely managed sanitation services can reduce diarrheal disease, and can significantly lessen the adverse health impacts of other disorders responsible for death and disease among millions of children. Diarrhea and worm infections weaken children and make them more susceptible to malnutrition and opportunistic infections like pneumonia, measles and malaria.





















The combined effects of inadequate sanitation, unsafe water supply and poor personal hygiene are responsible for many of childhood deaths. Every year, the failure to tackle these deficits results in severe welfare losses - wasted time, reduced productivity, ill health, impaired learning, environmental degradation and lost opportunities. Fundamental behavior changes are required before the use of improved facilities and services can be integrated into daily life. Many hygiene behaviors and habits are formed in childhood and, therefore, school health and hygiene education programs are an important part of water and sanitation improvements.





















Most basic sanitation technologies are not expensive to implement. However, those facing the problems of inadequate sanitation may not be aware of either the origin of their ills, or the true costs of poor sanitation and hygiene. As a result, in most of the developing countries those without sanitation are hard to convince of the need to invest scarce resources in sanitation facilities, or of the critical importance of changing long-held habits and unhygienic behaviors. Consequently, the people's representatives - governments and elected political leaders - rarely give sanitation or hygiene improvements the priority that is needed in order to tackle the massive sanitation deficit faced by the developing world.





















Children bear the brunt of sanitation-related impacts - their health, nutrition, growth, education, self-respect, and life opportunities suffer as a result of inadequate sanitation. Without improved sanitation, many of the current generation of children in developing countries are unlikely to develop to their full potential. Countries that don't take urgent action to redress sanitation deficiencies will find their future development and prosperity impaired.

### Limitations and exceptions:
National, regional and income group estimates are made when data are available for at least 50 percent of the population.

### Source

#### WHO/UNICEF Joint Monitoring Programme for Water Supply, Sanitation and Hygiene (JMP), via World Bank – World Development Indicators
Retrieved on: 2026-02-27  
Retrieved from: https://data.worldbank.org/indicator/SH.STA.BASS.ZS  


    