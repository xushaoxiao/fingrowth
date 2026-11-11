# Connect an aggregate source

FinGrowth can refresh the registration-to-credit funnel from an HTTP endpoint or a read-only MCP tool. Both use the [registration-to-credit intake contract](../skills/growth-funnel-diagnosis/references/registration-credit.md) and the same calculator. This view needs five ordered population counts and a fixed follow-up window. Unit economics and the broader lending workspace use their own contract.

## Run the Argentina demo

Run these commands from the repository root. Keep the source and dashboard commands running in separate terminals.

```sh
npm --prefix dashboard ci
npm --prefix dashboard run build
python3 -m examples.argentina.mock_aggregate
```

Start FinGrowth in another terminal.

```sh
python3 -m scripts.serve_dashboard --config examples/argentina/sources.json
```

Open [the dashboard](http://127.0.0.1:4173/), select **Registration to credit**, choose **Argentina demo · HTTP**, and select **Refresh data**. The mock source reports 1,000 registered, 700 with profile complete, 560 who passed KYC, 280 with bank details complete and 224 approved. The overall conversion is **22.40%** for the January 2026 registration cohort, observed through February 7 with seven days of fixed follow-up in Buenos Aires.

For the MCP demo, install the optional dependencies into a virtual environment and run the mock tool in another terminal.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-mcp.txt
.venv/bin/python -m examples.argentina.mock_mcp
```

Restart the FinGrowth dashboard server with `.venv/bin/python -m scripts.serve_dashboard --config examples/argentina/sources.json`. Select **Argentina demo · MCP** and refresh. The example exposes the same aggregate through `registration_credit_aggregate` over Streamable HTTP. [MCP Python SDK transport documentation](https://py.sdk.modelcontextprotocol.io/client/transports/)

## Configure a project

Copy [the source configuration](../examples/argentina/sources.json) to a local file. The top-level keys identify the sources in the Dashboard. Update a source's `label`, `transport` and `url`. HTTP uses GET and expects JSON. MCP uses a Streamable HTTP endpoint, a fixed `tool` name, optional JSON object `arguments` and a structured object result. For bearer authentication, set `bearer_token_env` to the name of an environment variable and supply the token to the FinGrowth process. Use HTTPS for remote endpoints and HTTP for local demos.

If the response already matches the intake contract, omit `mapping`. Use `payload_path` when the object is inside a response envelope, such as `data.funnel`.

For an existing project-specific aggregate, use the data-adapter Skill to compare a reviewed sample with the five stage definitions. Save a [mapping profile](../examples/argentina/mapping.json) and its [intake template](../examples/argentina/intake-template.json). The template declares the source, cohort population, stage definitions and follow-up policy. The mapping copies five counts, three window dates and the extraction timestamp from the current response. Use a separate configuration whenever the population or metric definitions differ. Source-side aggregation must establish the ordered unique-person populations and apply the documented follow-up. Mapping paths are dotted object keys.

The `mapping` path is relative to the source configuration file. The `template` path is relative to the mapping file. Restart FinGrowth after editing these files. A refresh validates the full intake and updates the saved result only after success. Failed refreshes display an error and retain that source's last successful result, including its timestamps. The service keeps these results in memory across browser reloads until the service restarts.

The source connection runs in the localhost FinGrowth process. The browser receives the validated report and source metadata. Keep project credentials and source configuration containing private details in your local environment.

## Verify locally

```sh
.venv/bin/python -m unittest discover -s tests -p test_connected_funnel.py -v
```

The integration test compares HTTP and MCP outputs using the same mapping and verifies that a failed refresh preserves the last valid result.
