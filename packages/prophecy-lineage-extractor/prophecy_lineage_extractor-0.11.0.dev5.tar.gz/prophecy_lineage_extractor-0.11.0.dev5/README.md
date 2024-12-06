# Prophecy Lineage Extractor

## Running

* Please run extractor as following, it needs env variables
* we Only need to set SMTP creds if we plan to pass `--send-email` argument

```shell
export PROPHECY_URL=https://app.prophecy.io
export PROPHECY_PAT=${{ secrets.PROPHECY_PAT }}

export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=${{ secrets.SMTP_USERNAME }}
export SMTP_PASSWORD=${{ secrets.SMTP_PASSWORD }}
export RECEIVER_EMAIL=ashish@prophecy.io
python -m prophecy_lineage_extractor --project-id 36587 --pipeline-id 36587/pipelines/customer_orders_demo --send-email
```

## Github Action Guide

* This extactor can be setup in Github Action of a Prophecy project to get email of lineage on every commit to main
* Following is a sample of github action we can use

```yaml
name: Run Prophecy Lineage extractor and send output to email

on:
  push:
    branches:
      - main  # Trigger on merge to the main branch
    paths:
      - 'datasets/**'
      - 'pipelines/**'
      - 'pbt_proect.yml'
      - '.github/workflows/prophecy_lineage_extractor.yml'
jobs:
  extract-and-mail-prophecy-lineage:
    runs-on: ubuntu-latest

    steps:
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'  # Adjust Python version as needed

      - name: Install Package from PyPI
        run: |
          pip install --no-cache-dir prophecy-lineage-extractor

      - name: Extract and Send Prophecy Lineage
        run: |
          export PROPHECY_URL=https://app.prophecy.io
          export PROPHECY_PAT=${{ secrets.PROPHECY_PAT }}
          
          export SMTP_HOST=smtp.gmail.com
          export SMTP_PORT=587
          export SMTP_USERNAME=${{ secrets.SMTP_USERNAME }}
          export SMTP_PASSWORD=${{ secrets.SMTP_PASSWORD }}
          export RECEIVER_EMAIL=ashish@prophecy.io
          python -m prophecy_lineage_extractor --project-id 36587 --pipeline-id 36587/pipelines/customer_orders_demo --send-email


```
