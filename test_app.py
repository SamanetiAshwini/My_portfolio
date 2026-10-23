"""
Comprehensive automated test suite for Ashwini Samaneti's Portfolio.
Tests API routes, validation rules, static files, and error handling.
"""

import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Samaneti Ashwini" in response.text
    assert "https://github.com/SamanetiAshwini/SkillTracker" in response.text
    print("[PASS] test_home_html")


def test_home_json_negotiation():
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    data = response.json()
    assert "Ashwini Samaneti" in data["message"]
    print("[PASS] test_home_json_negotiation")


def test_swagger_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()
    print("[PASS] test_swagger_docs")


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "healthy"
    assert "database_connected" in data
    assert "database_message" in data
    print(f"[PASS] test_api_health (DB connected: {data['database_connected']})")


def test_list_projects():
    response = client.get("/api/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 3
    slugs = [p["slug"] for p in projects]
    assert "codefoundry" in slugs
    assert "skilltrack" in slugs
    assert "smriti" in slugs
    print("[PASS] test_list_projects")


def test_filter_projects_by_tech():
    response = client.get("/api/projects?technology=Docker")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["slug"] == "codefoundry"
    print("[PASS] test_filter_projects_by_tech")


def test_get_project_detail_and_404():
    # Valid detail: CodeFoundry
    response = client.get("/api/projects/codefoundry")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "CodeFoundry"
    assert len(data["features"]) >= 3
    assert len(data["contributions"]) >= 3

    # Valid detail: SkillTrack (verifying GitHub URL)
    response_st = client.get("/api/projects/skilltrack")
    assert response_st.status_code == 200
    data_st = response_st.json()
    assert data_st["title"] == "SkillTrack"
    assert data_st["github_url"] == "https://github.com/SamanetiAshwini/SkillTracker"

    # Non-existent
    response_404 = client.get("/api/projects/unknown-proj")
    assert response_404.status_code == 404
    print("[PASS] test_get_project_detail_and_404")


def test_contact_form_validation():
    # Invalid email
    bad_email = client.post("/contact", json={
        "name": "Maya",
        "email": "notanemail",
        "message": "Valid message with more than 10 characters."
    })
    assert bad_email.status_code == 422

    # Name too short
    short_name = client.post("/contact", json={
        "name": "A",
        "email": "maya@example.com",
        "message": "Valid message with more than 10 characters."
    })
    assert short_name.status_code == 422

    # Message too short
    short_msg = client.post("/contact", json={
        "name": "Maya Sharma",
        "email": "maya@example.com",
        "message": "Hi"
    })
    assert short_msg.status_code == 422

    # Spam honeypot filled (website trap)
    spam_res = client.post("/contact", json={
        "name": "Spam Bot",
        "email": "spambot@example.com",
        "message": "Buy cheap backlinks today right now!",
        "website": "http://spamsite.com"
    })
    assert spam_res.status_code == 400
    print("[PASS] test_contact_form_validation")


def test_contact_unverified_db_handling():
    # Valid input payload
    payload = {
        "name": "Maya Sharma",
        "email": "maya@example.com",
        "subject": "Engineering Role",
        "message": "Hello Ashwini, we have an open Python backend engineer role for you."
    }
    response = client.post("/contact", json=payload)
    # If MongoDB is unconfigured or unreachable, it should honestly return 503 rather than fake success
    # If MongoDB is connected, it should return 201
    assert response.status_code in [201, 503]
    if response.status_code == 503:
        assert "unverified" in response.json()["detail"].lower() or "connectivity" in response.json()["detail"].lower()
    print(f"[PASS] test_contact_unverified_db_handling (Status code: {response.status_code})")


def test_chatbot_service():
    # Query about CodeFoundry
    res_cf = client.post("/api/chat", json={"message": "Tell me about CodeFoundry"})
    assert res_cf.status_code == 200
    data_cf = res_cf.json()
    assert "CodeFoundry" in data_cf["reply"]
    assert "Docker" in data_cf["reply"]

    # Query about SkillTrack
    res_st = client.post("/api/chat", json={"message": "Tell me about SkillTrack"})
    assert res_st.status_code == 200
    data_st = res_st.json()
    assert "SkillTrack" in data_st["reply"]
    assert "https://github.com/SamanetiAshwini/SkillTracker" in data_st["reply"]

    # Query about education
    res_edu = client.post("/api/chat", json={"message": "Where did you study?"})
    assert res_edu.status_code == 200
    data_edu = res_edu.json()
    assert "VJIT" in data_edu["reply"]
    assert "8.34" in data_edu["reply"]

    # Query about skills
    res_skills = client.post("/api/chat", json={"message": "What skills do you know?"})
    assert res_skills.status_code == 200
    data_skills = res_skills.json()
    assert "FastAPI" in data_skills["reply"]
    assert "Django" in data_skills["reply"]
    # Query about certifications
    res_cert = client.post("/api/chat", json={"message": "What certifications do you have?"})
    assert res_cert.status_code == 200
    data_cert = res_cert.json()
    assert "AWS Academy Graduate" in data_cert["reply"]
    assert "PCAP" in data_cert["reply"]
    assert "Cognitive Class" in data_cert["reply"]
    assert "Infosys" in data_cert["reply"]
    print("[PASS] test_chatbot_service")


def test_static_resume_file():
    res = client.get("/static/docs/Samaneti_Ashwini_Resume.pdf")
    assert res.status_code == 200
    assert len(res.content) > 100000  # verified PDF size ~305KB
    print(f"[PASS] test_static_resume_file ({len(res.content)} bytes)")


def test_static_certificates():
    certs = [
        "/static/images/certificate-aws-ml.png",
        "/static/images/certificate-cisco-pcap.png",
        "/static/images/certificate-ibm-python.png",
        "/static/images/certificate-hexart-ai.png",
        "/static/images/certificate-infosys-nlp.png",
        "/static/images/smriti-certificate.jpg"
    ]
    for cert_url in certs:
        res = client.get(cert_url)
        assert res.status_code == 200, f"Failed to load certificate: {cert_url}"
        assert len(res.content) > 10000, f"Certificate file too small: {cert_url}"
    print(f"[PASS] test_static_certificates ({len(certs)} verified certificates loaded)")


def test_sitemap_xml():
    res = client.get("/sitemap.xml")
    assert res.status_code == 200
    assert "application/xml" in res.headers["content-type"]
    assert "#certifications" in res.text
    print("[PASS] test_sitemap_xml")


if __name__ == "__main__":
    print("Starting automated test suite...\n")
    test_home_html()
    test_home_json_negotiation()
    test_swagger_docs()
    test_api_health()
    test_list_projects()
    test_filter_projects_by_tech()
    test_get_project_detail_and_404()
    test_contact_form_validation()
    test_contact_unverified_db_handling()
    test_chatbot_service()
    test_static_resume_file()
    test_static_certificates()
    test_sitemap_xml()
    print("\nALL 13 AUTOMATED TESTS PASSED SUCCESSFULLY!")

