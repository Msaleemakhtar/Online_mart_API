from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException


from uuid import UUID
from unittest.mock import patch, AsyncMock
import pytest
from sqlmodel import Session, SQLModel, create_engine

# relative imports
from app.main import app
from app.core import settings
from app.core.config_db import get_db
from app.core.utils import get_password_hash
from app.models import LoginResponse, UserInDb, UserOutput, UserRegister





connection_string = str(settings.TEST_DB_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_string)


SQLModel.metadata.create_all(engine)


def get_session_override():
    with Session(engine) as session:
        return session

app.dependency_overrides[get_db] = get_session_override
client = TestClient(app=app)


@pytest.fixture
def mock_user_db():
    test_password = "testpasword"
    hashed_password = get_password_hash(test_password)
    return UserInDb(
        id=UUID("845fe9c6-9e1c-4b93-8498-57fa920a07d0"),
        hashed_password=hashed_password,
        username="test",
        full_name="testapi",
        email="testapi@example.com",
        email_verified=True
    )

@pytest.fixture
def mock_user_output(mock_user_db):
    return UserOutput(
        id=mock_user_db.id,
        username=mock_user_db.username,
        full_name=mock_user_db.full_name,
        email=mock_user_db.email,
        email_verified=mock_user_db.email_verified
    )

@pytest.fixture
def mock_create_access_token():
    expected_code = "testcode"
    with patch('app.main.create_access_token', return_value = expected_code):
        yield expected_code


@pytest.fixture
def mock_login_response(mock_user_output):
    return LoginResponse(
        user=mock_user_output,
        access_token="testtoken",
        token_type="bearer"
    )

# endpoints for 0auth2 authentication

def test_signup_missing_fullname(): 
    response = client.post("/api/oauth/signup", json={"email": "test1@example.com", "username": "test1"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'type': 'missing', 
                                           'loc': ['body', 'full_name'], 
                                           'msg': 'Field required', 
                                           'input': {'email': 'test1@example.com', 'username': 'test1'}, 
                                           'url': 'https://errors.pydantic.dev/2.6/v/missing'},
                                             {'type': 'missing', 'loc': ['body', 'password'], 
                                              'msg': 'Field required', 
                                              'input': {'email': 'test1@example.com', 'username': 'test1'}, 
                                              'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}


# Test login with incomplete data: Send incomplete form data and assert validation errors.
def test_login_missing_data():
    response = client.post("/api/oauth/login", json={"username": "test"})
    assert response.status_code == 422
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) > 0
    assert "type" in response_data["detail"][0]
    assert response_data['detail'][0]['msg'] == 'Field required'
    assert response_data['detail'][0]['type'] == 'missing'
    assert response_data['detail'][0]['url'] == 'https://errors.pydantic.dev/2.6/v/missing'
    assert response_data['detail'][1]['loc'] == ['body', 'password']



#"/api/oauth/token"
def test_get_temp_code():
    user_id = UUID("845fe9c6-9e1c-4b93-8498-57fa920a07d0")
    expected_code = "testcode"
    with patch('app.main.create_access_token', return_value = expected_code):
        response = client.get(f"/api/oauth/get_temp_code?user_id={user_id}")
        assert response.status_code == 200
        response_data = response.json()
        assert "code" in response_data
        assert response_data["code"] == expected_code



def test_get_temp_code_fixture(mock_create_access_token):
    user_id = UUID("845fe9c6-9e1c-4b93-8498-57fa920a07d0")
    expected_code = mock_create_access_token
    response = client.get(f"/api/oauth/get_temp_code?user_id={user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert "code" in response_data
    assert response_data["code"] == expected_code



def test_token_manager_outh_flow_granttype_missing():
    response = client.post("/api/oauth/token", json={"code": "testcode"})
    print(response.json())
    assert response.status_code == 422
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) > 0
    assert response_data["detail"][0]["loc"] == ["body", "grant_type"]
    assert response_data["detail"][0]["msg"] == "Field required"
    assert response_data["detail"][0]["type"] == "missing"
    assert response.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'grant_type'], 
                                           'msg': 'Field required', 'input': None, 
                                           'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}
    


           
            
def test_tokens_manager_oauth_code_flow_with_failed_refresh_token():

    # Mock gpt_tokens_service to raise an HTTPException for an invalid or expired token
    with patch('app.service.get_gpt_token') as mock_service:
        mock_service.side_effect = HTTPException(status_code=401, detail="Token invalid or expired")

        response = client.post(
            "/api/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": "testcode"
            }
        )

        # Assert that the response status code is 401 (Unauthorized)
        assert response.status_code == 401
        response_data = response.json()
        print(response_data)

        # Assert the error message is in the response
        assert "detail" in response_data
        assert response_data["detail"] == {"error": "access_token", "error_description":"The access token expired" }



def test_tokens_manager_oauth_code_flow_with_refresh_token():
   
    # Mock get_gpt_token to return a valid token
    Mock_response ={
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
        "token_type": "Bearer"

    }
    # await validate_refresh_token(refresh_token)
    with patch('app.service.validate_refresh_token', new_callable=AsyncMock, return_value= "user_id"):
        with patch('app.service.get_gpt_token',  return_value= Mock_response):
            response = client.post(
                "/api/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": "testcode"
                }
            )

            # Assert that the response status code is 200 (OK)
            assert response.status_code == 200
            response_data = response.json()
            print(response_data)

            # Assert the response data is as expected
            assert "access_token" in response_data
            assert "refresh_token" in response_data
            assert "expires_in" in response_data
            assert "token_type" in response_data

       