for file in src/aind_data_schema_models/_generators/templates/*.txt; do
    # Extract the filename without the directory and extension
    type_name=$(basename "$file" .txt)
    
    # Call the Python script with the --type parameter
    python src/aind_data_schema_models/_generators/generator.py --type "$type_name"
done