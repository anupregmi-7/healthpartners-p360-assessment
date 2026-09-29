# HealthPartners P360 Data Engineering Assessment

Assessment submission by Anup Regmi.

## Files

- `code/cms_hospital_data_pipeline.py`: Python pipeline for CMS Hospital datasets.
- `model/Restaurant_Data_Model.drawio`: Editable restaurant data model (draw.io XML).
- `model/Restaurant_Data_Model. draw-io.pdf`: PDF export of the data model.

## Run the Python pipeline

Requires Python 3 and internet access. Uses only Python standard-library modules.

```sh
cd code
python3 cms_hospital_data_pipeline.py
```

The script retrieves CMS dataset metadata, selects datasets whose theme includes `Hospitals`, and processes new or modified datasets in parallel. CSV column names are normalized to snake_case. Processed CSVs are written to `output/`, and dataset modification timestamps are saved in `state.json` for subsequent runs.

## Validation

Python syntax and draw.io XML parsing were checked before packaging. The pipeline has not been executed against the live CMS service as part of packaging.
