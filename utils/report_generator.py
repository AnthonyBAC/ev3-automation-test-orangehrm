import base64
import json
import logging
import os
import time
import html as html_lib
from datetime import datetime
from pathlib import Path


REPORT_JSON = "reports/report.json"
ERRORS_JSON = "reports/errors.json"
SCREENSHOTS_DIR = "reports/screenshots"
FAIL_DIR = "reports/fail"
HTML_DIR = "reports/html"
HTML_FILE = "reports/html/report.html"


def _encode_image(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"


def _safe_filename(name):
    return name.replace(" ", "_").replace("/", "_") + ".png"


def _esc(text):
    return html_lib.escape(str(text)) if text else ""


def _status_badge(status):
    classes = {
        "passed": "text-success-emphasis bg-success-subtle",
        "failed": "text-danger-emphasis bg-danger-subtle",
        "error": "text-danger-emphasis bg-danger-subtle",
        "skipped": "text-info-emphasis bg-info-subtle",
        "undefined": "text-warning-emphasis bg-warning-subtle",
    }
    labels = {
        "passed": "Passed",
        "failed": "Failed",
        "error": "Error",
        "skipped": "Skipped",
        "undefined": "Undefined",
    }
    cls = classes.get(status, "text-secondary-emphasis bg-secondary-subtle")
    label = labels.get(status, status)
    return f'<span class="badge log {cls}">{label}</span>'


def generate_html_report():
    data = None
    for attempt in range(5):
        try:
            with open(REPORT_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            break
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Intento {attempt + 1} de leer report.json: {e}")
            time.sleep(1)

    if data is None:
        logging.error("No se pudo leer report.json para generar el HTML")
        return None

    Path(HTML_DIR).mkdir(parents=True, exist_ok=True)

    errors_data = []
    if os.path.exists(ERRORS_JSON):
        try:
            with open(ERRORS_JSON, "r", encoding="utf-8") as f:
                errors_data = json.load(f)
        except json.JSONDecodeError:
            errors_data = []

    error_lookup = {
        (item.get("feature", ""), item.get("scenario", ""), item.get("step", "")): item.get("error", "")
        for item in errors_data
    }

    total_features = 0
    passed_features = 0
    failed_features = 0
    total_scenarios = 0
    passed_scenarios = 0
    failed_scenarios = 0
    skipped_scenarios = 0
    total_steps = 0
    passed_steps = 0
    failed_steps = 0
    skipped_steps = 0

    features = []
    errors_list = []
    feature_idx = 0

    for feature in data:
        if not isinstance(feature, dict):
            continue
        feature_idx += 1
        total_features += 1
        f_name = feature.get("name", "")
        f_status = feature.get("status", "unknown")
        f_tags = feature.get("tags", [])
        if f_status == "passed":
            passed_features += 1
        else:
            failed_features += 1

        f_passed = 0
        f_failed = 0
        scenarios = []
        for scenario in feature.get("elements", []):
            total_scenarios += 1
            s_name = scenario.get("name", "")
            s_status = scenario.get("status", "unknown")
            s_tags = scenario.get("tags", [])
            if s_status == "passed":
                passed_scenarios += 1
                f_passed += 1
            elif s_status in ("failed", "error"):
                failed_scenarios += 1
                f_failed += 1
            else:
                skipped_scenarios += 1

            s_passed_steps = 0
            s_failed_steps = 0
            s_skipped_steps = 0
            steps_html = ""
            for step in scenario.get("steps", []):
                total_steps += 1
                result = step.get("result", {})
                st_status = result.get("status", "skipped")
                keyword = step.get("keyword", "")
                st_name = step.get("name", "")
                error_msg = result.get("error_message", [])

                if st_status == "passed":
                    passed_steps += 1
                    s_passed_steps += 1
                elif st_status in ("failed", "error"):
                    failed_steps += 1
                    s_failed_steps += 1
                else:
                    skipped_steps += 1
                    s_skipped_steps += 1

                badge = _status_badge(st_status)
                error_html = ""
                error_text = error_lookup.get((f_name, s_name, f"{keyword} {st_name}"), "")
                if not error_text and error_msg:
                    error_text = "\n".join(error_msg) if isinstance(error_msg, list) else str(error_msg)
                if error_text:
                    error_html = f'<pre class="alert alert-danger mt-2"><code>{_esc(error_text)}</code></pre>'

                steps_html += f"""
                <div class="step-detail mb-2">
                    <p class="mb-0"><small>{badge} <span class="fw-semibold">{_esc(keyword)}</span> {_esc(st_name)}</small></p>
                    {error_html}
                </div>"""

            screenshot_path = os.path.join(SCREENSHOTS_DIR, _safe_filename(s_name))
            fail_screenshot_path = os.path.join(FAIL_DIR, _safe_filename(s_name))
            screenshot_b64 = _encode_image(screenshot_path)
            fail_screenshot_b64 = _encode_image(fail_screenshot_path) if s_status in ("failed", "error") else None

            is_known_issue = "known_issue" in s_tags

            screenshots_html = ""
            if screenshot_b64:
                screenshots_html += f'<div class="mt-2"><h6>Screenshot</h6><img src="{screenshot_b64}" class="img-fluid rounded border" alt="screenshot" style="max-height: 400px;"></div>'
            if fail_screenshot_b64:
                screenshots_html += f'<div class="mt-2"><h6>Screenshot del fallo</h6><img src="{fail_screenshot_b64}" class="img-fluid rounded border" alt="fail screenshot" style="max-height: 400px;"></div>'

            known_issue_banner = ""
            if is_known_issue:
                known_issue_banner = '<div class="alert alert-warning"><i class="bi bi-exclamation-triangle"></i> <strong>KNOWN ISSUE:</strong> Falla esperada y documentada</div>'

            tags_html = " ".join(f'<span class="badge text-warning-emphasis bg-warning-subtle fw-semibold">{_esc(t)}</span>' for t in s_tags)

            scenarios.append({
                "name": s_name,
                "status": s_status,
                "tags": s_tags,
                "tags_html": tags_html,
                "passed_steps": s_passed_steps,
                "failed_steps": s_failed_steps,
                "skipped_steps": s_skipped_steps,
                "total_steps": s_passed_steps + s_failed_steps + s_skipped_steps,
                "steps_html": steps_html,
                "screenshots_html": screenshots_html,
                "known_issue_banner": known_issue_banner,
                "is_known_issue": is_known_issue,
            })

        features.append({
            "idx": feature_idx,
            "name": f_name,
            "status": f_status,
            "tags": f_tags,
            "passed": f_passed,
            "failed": f_failed,
            "total": f_passed + f_failed,
            "scenarios": scenarios,
        })

    pass_rate = (passed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
    f_pass_rate = (passed_features / total_features * 100) if total_features > 0 else 0
    s_pass_rate = pass_rate
    st_pass_rate = (passed_steps / total_steps * 100) if total_steps > 0 else 0
    st_fail_rate = (failed_steps / total_steps * 100) if total_steps > 0 else 0
    st_skip_rate = (skipped_steps / total_steps * 100) if total_steps > 0 else 0

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Feature list items
    feature_items_html = ""
    for f in features:
        f_badge = _status_badge(f["status"])
        f_tags_str = ",".join(f["tags"])
        feature_items_html += f"""
        <li class="list-group-item border-end-0 border-start-0">
            <div class="test-detail" data-bs-toggle="collapse" role="button"
                 data-bs-target="#feature-{f['idx']}" aria-expanded="false" aria-controls="feature-{f['idx']}"
                 data-tags="{_esc(f_tags_str)}">
                <p class="fw-bolder feature-name">{_esc(f['name'])}</p>
                <p><small>{f_badge} <span>{f['passed']} passed / {f['failed']} failed / {f['total']} total</span></small></p>
            </div>
        </li>"""

    # Scenario detail panels
    scenario_panels_html = ""
    for f in features:
        scenarios_list_html = ""
        for sc in f["scenarios"]:
            s_badge = _status_badge(sc["status"])
            scenario_id = f"scenario_{f['idx']}_{scenarios_list_html.count('list-group-item')}"
            scenarios_list_html += f"""
            <li class="list-group-item" id="{scenario_id}">
                <div class="scenario-detail" data-tags="{_esc(','.join(sc['tags']))}" data-feature="{_esc(f['name'])}">
                    <p class="fw-bolder mb-1 scenario-name">{_esc(sc['name'])}</p>
                    <p><small>{s_badge}
                        <span class="badge text-success-emphasis bg-success-subtle log fw-semibold">Passed: {sc['passed_steps']}</span>
                        <span class="badge text-danger-emphasis bg-danger-subtle log fw-semibold">Failed: {sc['failed_steps']}</span>
                        <span class="badge text-info-emphasis bg-info-subtle log fw-semibold">Skipped: {sc['skipped_steps']}</span>
                        <span class="badge bg-light text-dark fw-semibold">Total: {sc['total_steps']}</span>
                    </small></p>
                    <div class="scenario-tags mb-1">{sc['tags_html']}</div>
                    {sc['known_issue_banner']}
                    <div class="steps-list mt-2">{sc['steps_html']}</div>
                    {sc['screenshots_html']}
                </div>
            </li>"""

        scenario_panels_html += f"""
        <div class="collapse show ps-2" id="feature-{f['idx']}" data-bs-parent="#scenariosList">
            <div class="detail-head pt-3">
                <div class="detail-head-title"><h4>{_esc(f['name'])}</h4></div>
                <div class="detail-head-info">
                    <p><small>{_status_badge(f['status'])}
                        <span class="fw-semibold badge log text-success-emphasis bg-success-subtle">Passed: {f['passed']}</span>
                        <span class="fw-semibold badge log text-danger-emphasis bg-danger-subtle">Failed: {f['failed']}</span>
                        <span class="fw-semibold badge log bg-light text-dark">Total: {f['total']}</span>
                    </small></p>
                </div>
                <hr>
            </div>
            <ul class="list-group scenarios-list-content">{scenarios_list_html}</ul>
        </div>"""

    if errors_data:
        errors_list = errors_data

    # Errors table rows
    error_rows_html = ""
    error_cards_html = ""
    for idx, err in enumerate(errors_list):
        error_type = "AssertionError" if err.get("status") == "failed" else "RuntimeError"
        error_rows_html += f"""
        <tr data-error-type="{_esc(error_type)}" data-step="{_esc(err['step'])}" data-scenario="{_esc(err['scenario'])}">
            <td>{_esc(err['feature'])}</td>
            <td><a href="#error_card_{idx}">{_esc(err['scenario'])}</a></td>
            <td><a href="#error_card_{idx}">{_esc(err['step'])}</a></td>
            <td>{_esc(error_type)}</td>
        </tr>"""
        error_cards_html += f"""
        <div class="card mt-3" id="error_card_{idx}" data-scenario="{_esc(err['scenario'])}">
            <div class="card-body">
                <h4>{_esc(err['scenario'])}</h4>
                <hr>
                <div class="card mt-3" data-step="{_esc(err['step'])}" data-error-type="{_esc(error_type)}">
                    <div class="card-body">
                        <h5>{_esc(err['step'])}</h5>
                        <p><strong>Exception type:</strong> {_esc(error_type)}</p>
                        <div class="error-message">
                            <h6>Error message:</h6>
                            <pre class="alert alert-danger"><code>{_esc(err['error'])}</code></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

    # Chart data
    feature_labels = [_esc(f["name"]) for f in features]
    feature_passed = [f["passed"] for f in features]
    feature_failed = [f["failed"] for f in features]

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OrangeHRM - Reporte de Pruebas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
            crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/echarts@6.0.0/dist/echarts.min.js"
            integrity="sha256-uqjf5+HZM2uY6Jhrp+IOoV582+oe9CpZ1ZR4Yy+kWh0=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
          integrity="sha256-9kPW/n5nn53j4WMRYAxe9c1rCY96Oogo/MKSVdKzPmI=" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"
            integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    <style>
        body {{ overflow-x: hidden; }}
        #header-navbar {{ background-color: #FF7B1D; border-bottom: 1px solid #f7fbff; }}
        .navbar-brand-wrapper {{ padding-top: 10px; padding-left: 25px; padding-bottom: 10px; }}
        .app {{ min-height: 100vh; }}
        .content {{ padding: 0; margin: 0; overflow: auto; min-height: 100%; }}
        #sidebarMenu {{ width: 235px; background-color: #f7fbff; position: fixed; height: calc(100vh); border-right: 1px solid #e9eaec; }}
        .full-container {{ min-height: 100vh; padding-left: 235px; padding-right: 0; }}
        .full-container .main-content {{ height: calc(100vh); min-height: calc(100vh); overflow-y: auto; }}
        .list-group {{ border-radius: unset; }}
        .badge.log {{ font-size: 100%; color: #f6f7f6; letter-spacing: -0.5px; }}
        .test-detail p {{ margin-bottom: unset; }}
        .features-list-content .list-group-item, .steps-list-content .list-group-item {{ cursor: pointer; }}
        #header-navbar.sidebar-mobile {{ display: none !important; }}
        @media (max-width: 768px) {{
            #sidebarMenu {{ z-index: 500; width: 100%; position: fixed; top: 75px; height: calc(100vh - 75px); left: 0; }}
            .full-container {{ padding-left: 0; padding-right: 0; }}
            .full-container .main-content {{ padding: 85px 15px 0 15px; }}
            #header-navbar.sidebar-mobile {{ display: flex !important; }}
            #headerLogoDesktop, hr {{ display: none; }}
        }}
        .scenarios-list > .collapsing, .steps-list > div.collapsing {{ -webkit-transition: none; transition: none; display: none; }}
        .main-content > div.collapsing {{ -webkit-transition: none; transition: none; display: none; }}
        .home-card-grid {{ position: relative; display: grid; grid-template-columns: max-content max-content; align-items: center; padding-left: 1em; grid-gap: 20px; }}
        .result-cards-container {{ display: grid; column-gap: 10px; grid-template-columns: 1fr 1fr 1fr 1fr; }}
        @media (max-width: 1510px) {{ .result-cards-container {{ grid-template-columns: 1fr 1fr; }} }}
        @media (max-width: 560px) {{ .result-cards-container {{ grid-template-columns: 1fr; }} .home-card-grid {{ grid-template-columns: max-content max-content; }} }}
        .home-card-grid p {{ margin-bottom: 0; }}
        .home-card-grid-green {{ background-color: #16958982; }}
        .home-card-grid-orange {{ background-color: #d76d0e8f; }}
        .home-card-grid-pink {{ background-color: #ed438069; }}
        .home-card-grid-blue {{ background-color: #6e79ff69; }}
        .home-card-grid-green i {{ color: #004535; }}
        .home-card-grid-orange i {{ color: #8d490c; }}
        .home-card-grid-pink i {{ color: #991746; }}
        .home-card-grid-blue i {{ color: #00086ddb; }}
        .home-card-grid-left-box {{ padding: 1.5em; padding-left: 2em; padding-right: 2em; border-radius: 15px; }}
        .home-card-grid-left-box i {{ font-size: 2em; }}
        .card {{ border: 0; box-shadow: -2px -2px 8px 0 rgba(255,255,255,0.5), 2px 2px 8px 0 rgba(180,193,200,0.66); }}
        .nav-link {{ border-radius: 8px; }}
        .sidebar .nav-link {{ width: 100%; font-weight: 500; color: #6C7383; position: relative; display: grid; grid-template-columns: max-content max-content max-content; align-items: center; grid-gap: 5px; margin-bottom: 5px; }}
        #sidebarMenu button[aria-expanded="true"], .sidebar .nav-link.active, .sidebar .nav-link:hover {{ background-color: #FF7B1D; color: #ffffff; font-weight: 700; border-radius: 8px; }}
        li:has(div.test-detail[aria-expanded="true"]) {{ background-color: #FF7B1D30; }}
        .table-dark {{ --bs-table-bg: #FF7B1D; --bs-table-border-color: #ffffff; }}
        .scrollable_table {{ overflow-y: auto; height: calc(44vh); }}
        .overview-card {{ height: calc(55vh); max-height: calc(55vh); }}
        @media (min-width: 992px) {{
            div#features_list_view, div#steps_list_view {{ overflow: hidden; height: calc(95vh); max-height: calc(100vh); }}
            .list-group.scenarios-list-content {{ height: calc(80vh); overflow: auto; margin-bottom: 15px; }}
            .features-list-content .list-group, .steps-list-content .list-group {{ height: calc(93vh); overflow: auto; overflow-x: hidden; }}
        }}
        .list-group.scenarios-list-content {{ margin-bottom: 15px; }}
        .scenario-detail {{ padding: 10px 0; }}
        .step-detail {{ padding: 5px 10px; background: #f8f9fa; border-radius: 4px; margin-bottom: 5px; }}
        .step-detail pre {{ margin-bottom: 0; max-height: 300px; overflow-y: auto; }}
        .scenario-tags {{ display: flex; gap: 5px; flex-wrap: wrap; }}
    </style>
</head>
<body id="body-pd">
<div class="app">
    <div class="row">
        <header id="header-navbar" class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row sidebar-mobile mb-3">
            <div class="text-center navbar-brand-wrapper d-flex align-items-center justify-content-start">
                <a href="#" class="text-white text-decoration-none fs-4 fw-bold">OrangeHRM Test Report</a>
            </div>
            <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end p-3">
                <button class="navbar-toggler position-relative d-md-none ms-auto collapsed" type="button"
                        data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
        </header>

        <nav id="sidebarMenu" class="col-lg-3 d-md-block p-3 sidebar collapse" role="navigation">
            <div class="ps-3">
                <a href="#" class="text-decoration-none fs-5 fw-bold text-dark">OrangeHRM</a>
            </div>
            <div class="p-3 menu-items">
                <hr>
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <button disabled type="button" title="Overview" class="nav-link"
                                data-bs-toggle="collapse" data-bs-target="#overview_view" aria-expanded="true"
                                aria-controls="overview_view" aria-current="page">
                            <i class="bi bi-clipboard-data"></i>
                            <span>Overview</span>
                        </button>
                    </li>
                    <li class="nav-item">
                        <button type="button" id="test-suite-button" title="Features" class="nav-link"
                                aria-current="page"
                                data-bs-toggle="collapse" data-bs-target="#features_list_view" aria-expanded="false"
                                aria-controls="features_list_view">
                            <i class="bi bi-box-seam"></i>
                            <span>Test Suites</span>
                        </button>
                    </li>
                    <li class="nav-item">
                        <button type="button" id="errors-button" title="Errors" class="nav-link"
                                aria-current="page"
                                data-bs-toggle="collapse" data-bs-target="#errors_list_view" aria-expanded="false"
                                aria-controls="errors_list_view">
                            <i class="bi bi-bug"></i>
                            <span>Errors</span>
                        </button>
                    </li>
                </ul>
            </div>
        </nav>

        <div class="full-container">
            <div class="main-content" id="mainContent" role="main">

<!-- OVERVIEW -->
<div class="row content collapse show" id="overview_view" data-bs-parent="#mainContent">
    <div class="col-lg-12 p-4">
        <div class="row">
            <div class="col-sm-12 col-md-12 col-lg-12 col-xl-12 mb-4">
                <div class="result-cards-container">
                    <div class="card mb-4">
                        <div class="card-body">
                            <div class="row home-card-grid">
                                <div class="home-card-grid-left-box home-card-grid-green">
                                    <i class="bi bi-box-seam"></i>
                                </div>
                                <div>
                                    <h3>{total_features}</h3>
                                    <p>Test Suites Executed</p>
                                </div>
                            </div>
                            <div class="progress-stacked mt-4">
                                <div class="progress" role="progressbar" style="width: {f_pass_rate:.2f}%;" aria-valuenow="{f_pass_rate:.2f}" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar bg-success">{f_pass_rate:.2f}%</div>
                                </div>
                                <div class="progress" role="progressbar" style="width: {100 - f_pass_rate:.2f}%;" aria-valuenow="{100 - f_pass_rate:.2f}" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar bg-danger">{100 - f_pass_rate:.2f}%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card mb-4">
                        <div class="card-body">
                            <div class="row home-card-grid">
                                <div class="home-card-grid-left-box home-card-grid-orange">
                                    <i class="bi bi-boxes"></i>
                                </div>
                                <div>
                                    <h3>{total_scenarios}</h3>
                                    <p>Test Cases Executed</p>
                                </div>
                            </div>
                            <div class="progress-stacked mt-4">
                                <div class="progress" role="progressbar" style="width: {s_pass_rate:.2f}%;" aria-valuenow="{s_pass_rate:.2f}" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar bg-success">{s_pass_rate:.2f}%</div>
                                </div>
                                <div class="progress" role="progressbar" style="width: {(failed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0:.2f}%;" aria-valuenow="{(failed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0:.2f}" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar bg-danger">{(failed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0:.2f}%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card mb-4">
                        <div class="card-body">
                            <div class="row home-card-grid">
                                <div class="home-card-grid-left-box home-card-grid-pink">
                                    <i class="bi bi-file-code"></i>
                                </div>
                                <div>
                                    <h3>{total_steps}</h3>
                                    <p>Steps Executed</p>
                                </div>
                            </div>
                            <div class="progress-stacked mt-4">
                                <div class="progress" role="progressbar" style="width: {st_pass_rate:.2f}%;" aria-valuenow="{st_pass_rate:.2f}" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar bg-success">{st_pass_rate:.2f}%</div>
                                </div>
                                <div class="progress" role="progressbar" style="width: {st_fail_rate:.2f}%;" aria-valuenow="{st_fail_rate:.2f}" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar bg-danger">{st_fail_rate:.2f}%</div>
                                </div>
                                <div class="progress" role="progressbar" style="width: {st_skip_rate:.2f}%;" aria-valuenow="{st_skip_rate:.2f}" aria-valuemin="0" aria-valuemax="100">
                                    <div class="progress-bar bg-info">{st_skip_rate:.2f}%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card mb-4">
                        <div class="card-body">
                            <div class="row home-card-grid">
                                <div class="home-card-grid-left-box home-card-grid-blue">
                                    <i class="bi bi-graph-up"></i>
                                </div>
                                <div>
                                    <h3>{pass_rate:.1f}%</h3>
                                    <p>Pass Rate</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-sm-12 col-md-12 col-lg-6 col-xl-6 mb-4">
                <div class="mb-4">
                    <div class="card">
                        <div class="card-body overview-card">
                            <h3>Execution Info</h3>
                            <div class="table-responsive scrollable_table">
                                <table class="table table-sm">
                                    <tr><th>Execution date:</th><td>{now}</td></tr>
                                    <tr><th>Tool:</th><td>behave + Selenium</td></tr>
                                    <tr><th>Engine:</th><td>behave</td></tr>
                                    <tr><th>Run type:</th><td>sequential</td></tr>
                                    <tr><th>Browser:</th><td>Chrome</td></tr>
                                    <tr><th>Total features:</th><td>{total_features}</td></tr>
                                    <tr><th>Total scenarios:</th><td>{total_scenarios}</td></tr>
                                    <tr><th>Total steps:</th><td>{total_steps}</td></tr>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-sm-12 col-md-12 col-lg-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h3>Feature - Scenario Results</h3>
                        <hr>
                        <div id="features_status" style="height: 500px;"></div>
                        <script>
                            $(document).ready(function() {{
                                const featureLabels = {json.dumps(feature_labels)};
                                let options = {{
                                    xAxis: {{ max: 'dataMax' }},
                                    yAxis: {{
                                        type: 'category', data: featureLabels, inverse: true, max: 'dataMax',
                                        axisLabel: {{
                                            width: 100, overflow: 'ellipsis',
                                            formatter: function(value) {{
                                                return value.length > 25 ? value.substring(0, 25) + '...' : value;
                                            }}
                                        }}
                                    }},
                                    tooltip: {{
                                        trigger: 'axis', axisPointer: {{ type: 'shadow' }},
                                        formatter: function(params) {{
                                            let yLabel = params[0] && params[0].axisValueLabel ? params[0].axisValueLabel : '';
                                            let content = `<b>${{yLabel}}</b><br/>`;
                                            params.forEach(function(item) {{
                                                if (item.value !== 0) content += `${{item.marker}} ${{item.seriesName}}: ${{item.value}}<br/>`;
                                            }});
                                            return content;
                                        }}
                                    }},
                                    series: [
                                        {{ name: "Passed Scenarios", type: 'bar', stack: 'y', data: {json.dumps(feature_passed)}, color: "#198754",
                                           label: {{ show: true, formatter: function(p) {{ return p.value === 0 ? '' : p.value; }} }} }},
                                        {{ name: "Failed Scenarios", type: 'bar', stack: 'y', data: {json.dumps(feature_failed)}, color: '#dc3545',
                                           label: {{ show: true, formatter: function(p) {{ return p.value === 0 ? '' : p.value; }} }} }}
                                    ],
                                    legend: {{ show: true }},
                                    toolbox: {{ show: true, feature: {{ saveAsImage: {{}}, restore: {{}}, dataZoom: {{}} }} }}
                                }};
                                echarts.init(document.querySelector("#features_status")).setOption(options);
                            }});
                        </script>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- TEST SUITES -->
<div class="row content collapse" id="features_list_view" data-bs-parent="#mainContent">
    <div class="col-lg-3 features-list p-0 border-end">
        <div class="d-flex">
            <form class="features-list-tools w-100">
                <ul class="list-group border-0">
                    <li class="list-group-item border-0">
                        <div class="row g-3 align-items-center features-filter">
                            <div class="col-12">
                                <div class="input-group">
                                    <div class="input-group-text"><i class="bi bi-search"></i></div>
                                    <input name="test-suite-name" type="text" class="form-control" id="test-suite-name" placeholder="Filter by test suite name">
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
                <div class="features-list-content">
                    <ul class="list-group">
                        {feature_items_html}
                    </ul>
                </div>
            </form>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="scenarios-list" id="scenariosList">
            {scenario_panels_html}
        </div>
    </div>
</div>

<!-- ERRORS -->
<div class="row content collapse" id="errors_list_view" data-bs-parent="#mainContent">
    <div class="col-12">
        <div class="card mt-3">
            <div class="card-body">
                <h3>Exceptions raised during execution</h3>
                <hr>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead class="table-dark">
                            <tr>
                                <th>Feature name</th>
                                <th>Scenario name</th>
                                <th>Step name</th>
                                <th>Exception type</th>
                            </tr>
                        </thead>
                        <tbody>
                            {error_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        {error_cards_html}
    </div>
</div>

            </div>
        </div>
    </div>
</div>

<script type="application/javascript">
    $(document).ready(function () {{
        let previousButton = $("button:disabled");
        $('.nav-link').on('click', function (_event) {{
            if (previousButton) $(previousButton).removeAttr('disabled');
            $(this).attr('disabled', 'disabled');
            previousButton = this;
        }});

        // Feature filter
        const $featureNameInput = $('#test-suite-name');
        const $featureItems = $('.features-list-content .list-group-item');
        $featureNameInput.on('input', function() {{
            const nameFilter = $(this).val().toLowerCase();
            $featureItems.each(function () {{
                const featureName = $(this).find('.feature-name').text().toLowerCase();
                $(this).toggle(featureName.includes(nameFilter));
            }});
        }});

        // Click first feature to show by default
        $('.test-detail').first().trigger('click');
    }});
</script>
</body>
</html>"""

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    return HTML_FILE
