from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, hour, dayofweek, month, col, count, when, isnull, year
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import to_timestamp
from pyspark.ml.evaluation import ClusteringEvaluator

# Initialize Spark session
spark = SparkSession.builder.appName("Urban Crime Analysis").getOrCreate()
print('Spark Session initialized:', spark)

# Load data from HDFS
hdfs_path = "hdfs:///user/amoeed/big-data-project/Crimes_-_2001_to_Present.csv"
df = spark.read.csv(hdfs_path, header=True, inferSchema=True)

# Display schema and initial rows
df.printSchema()
df.show(5)

# Step 1: Data Cleaning
# Check for missing values
missing_values = df.select([count(when(isnull(c), c)).alias(c) for c in df.columns])
missing_values.show()

# Drop rows with missing critical data
df = df.dropna(subset=["Primary Type", "Date", "Latitude", "Longitude"])
df = df.withColumn("parsed_date", to_timestamp("Date", "MM/dd/yyyy hh:mm:ss a"))
df = df.withColumn("Month", month(col("parsed_date")))
df = df.withColumn("Hour", hour(col("parsed_date")))
df = df.withColumn("DayOfWeek", dayofweek(col("parsed_date")))
df = df.withColumn("Year", year(col("parsed_date")))
crime_by_area = df.groupBy("Community Area").count().orderBy("count", ascending=False)
crime_by_area.show()

# Count crimes by month (Crime trends over months)
crime_by_month = df.groupBy("Month").count().orderBy("Month")
crime_by_month.show()

# Analysis: Arrests per Month
arrest_monthly = df.groupBy(month(col("parsed_date")).alias("Month")) \
                   .agg(count(when(col("Arrest") == True, 1)).alias("Arrests")) \
                   .orderBy("Month")

arrest_monthly.show()

# Analysis: Domestic Issues per Month
domestic_monthly = df.groupBy(month(col("parsed_date")).alias("Month")) \
                     .agg(count(when(col("Domestic") == True, 1)).alias("Domestic_Issues")) \
                     .orderBy("Month")

domestic_monthly.show()

# Analysis: Crime Types per Month
crime_type_monthly = df.groupBy("Primary Type", "Month") \
                     .count() \
                     .orderBy("Month", "Primary Type")

crime_type_monthly.show()

# Analysis: Hourly Crime Trends
hourly_crime = df.groupBy("Hour").count().orderBy("Hour")
hourly_crime.show()

# Analysis: Crime Resolution (Arrest Rate by Crime Type)
arrest_rate_by_crime = df.groupBy("Primary Type") \
                        .agg(count(when(col("Arrest") == True, 1)).alias("Arrests"), 
                             count("Primary Type").alias("Total_Crimes")) \
                        .withColumn("Arrest_Rate", col("Arrests") / col("Total_Crimes")) \
                        .orderBy("Arrest_Rate", ascending=False)

arrest_rate_by_crime.show()
day_of_week_trends = df.groupBy("DayOfWeek").count().orderBy("DayOfWeek")
day_of_week_trends.show()
annual_trends = df.groupBy("Year").count().orderBy("Year")
annual_trends.show()
arrest_rate_by_year = df.groupBy("Year") \
                        .agg(count(when(col("Arrest") == True, 1)).alias("Arrests"), 
                             count("Year").alias("Total_Crimes")) \
                        .withColumn("Arrest_Rate", col("Arrests") / col("Total_Crimes")) \
                        .orderBy("Year")

arrest_rate_by_year.show()

# Step 4: Clustering for High-Risk Area Prediction
# Feature engineering for clustering
feature_cols = ["Latitude", "Longitude"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df_features = assembler.transform(df)

# Apply K-Means clustering
kmeans = KMeans(k=5, seed=1)
model = kmeans.fit(df_features)
clusters = model.transform(df_features)

# Step 5: Clustering Results Interpretation (Add labels for cluster predictions)
cluster_centers = model.clusterCenters()
cluster_labels = []
for i, center in enumerate(cluster_centers):
    if center[0] > 41.0 and center[1] > -87.5:  # Example for high-risk area near the city center
        cluster_labels.append(f"Cluster {i}: High Risk")
    else:
        cluster_labels.append(f"Cluster {i}: Low Risk")

# Assign human-readable labels based on clustering output
clusters = clusters.withColumn("Risk_Level", when(clusters["prediction"] == 0, cluster_labels[0])
                               .when(clusters["prediction"] == 1, cluster_labels[1])
                               .when(clusters["prediction"] == 2, cluster_labels[2])
                               .when(clusters["prediction"] == 3, cluster_labels[3])
                               .when(clusters["prediction"] == 4, cluster_labels[4])
                               .otherwise("Unknown"))

# Show clusters with readable labels
clusters.select("Community Area", "Latitude", "Longitude", "prediction", "Risk_Level").show()

# Step 6: Model Evaluation (Clustering evaluator to assess cluster quality)
evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(clusters)
print(f"Silhouette score for the clustering: {silhouette}")

# Step 7: Export Results for Visualization
# Export aggregated results to HDFS
output_path_area = "hdfs:///user/amoeed/big-data-project/crime_by_area.csv"
crime_by_area.write.csv(output_path_area, header=True)

output_path_month = "hdfs:///user/amoeed/big-data-project/crime_by_month.csv"
crime_by_month.write.csv(output_path_month, header=True)

output_path_arrest = "hdfs:///user/amoeed/big-data-project/arrest_monthly.csv"
arrest_monthly.write.csv(output_path_arrest, header=True)

output_path_domestic = "hdfs:///user/amoeed/big-data-project/domestic_monthly.csv"
domestic_monthly.write.csv(output_path_domestic, header=True)

output_path_crime_type_monthly = "hdfs:///user/amoeed/big-data-project/crime_type_monthly.csv"
crime_type_monthly.write.csv(output_path_crime_type_monthly, header=True)

output_path_hourly_crime = "hdfs:///user/amoeed/big-data-project/hourly_crime.csv"
hourly_crime.write.csv(output_path_hourly_crime, header=True)

output_path_arrest_rate = "hdfs:///user/amoeed/big-data-project/arrest_rate_by_crime.csv"
arrest_rate_by_crime.write.csv(output_path_arrest_rate, header=True)

output_path_day_of_week_trends = "hdfs:///user/amoeed/big-data-project/day_of_week_trends.csv"
day_of_week_trends.write.csv(output_path_day_of_week_trends, header=True)

output_path_annual_trends = "hdfs:///user/amoeed/big-data-project/annual_trends.csv"
annual_trends.write.csv(output_path_annual_trends, header=True)

output_path_arrest_rate_by_year = "hdfs:///user/amoeed/big-data-project/arrest_rate_by_year.csv"
arrest_rate_by_year.write.csv(output_path_arrest_rate_by_year, header=True)

output_path_clusters = "hdfs:///user/amoeed/big-data-project/clusters.csv"
clusters.select("Community Area", "Latitude", "Longitude", "prediction", "Risk_Level").write.csv(output_path_clusters, header=True)

# Stop Spark session
spark.stop()

print("Crime pattern analysis and high-risk area prediction completed.")
