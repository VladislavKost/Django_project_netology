import pytest

from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_first_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    url = f"/api/v1/courses/{course[0].id}/"
    # Act
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == course[0].name


@pytest.mark.django_db
def test_all_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    # Act
    response = client.get("/api/v1/courses/")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for id, course in enumerate(data):
        assert course["name"] == courses[id].name


@pytest.mark.django_db
def test_filter_courses_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=15)
    filtered_course_id = courses[len(courses) // 2].id
    url = f"/api/v1/courses/?id={filtered_course_id}"
    # Act
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    data = response.json()
    for course in data:
        assert course["id"] == filtered_course_id


@pytest.mark.django_db
def test_filter_courses_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    filtered_course_name = courses[len(courses) // 2].name
    url = f"/api/v1/courses/?name={filtered_course_name}"
    # Act
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    data = response.json()
    for course in data:
        assert course["name"] == filtered_course_name


@pytest.mark.django_db
def test_create_course(client, course_factory):
    # Arrange
    url = f"/api/v1/courses/"
    # Act
    response = client.post(url, data={"name": "Math"}, format="json")
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Math"


@pytest.mark.django_db
def test_update_course(client):
    # Arrange
    url = f"/api/v1/courses/"
    # Act
    response = client.post(url, data={"name": "Math"}, format="json")
    # Assert
    assert response.status_code == 201
    data = response.json()
    course_id = data["id"]
    response_update = client.patch(
        f"{url}{course_id}/",
        data={"name": "History"},
        format="json",
        content_type="application/json",
    )
    updated_data = response_update.json()
    assert updated_data["name"] == "History"


@pytest.mark.django_db
def test_delete_course(client):
    # Arrange
    url = f"/api/v1/courses/"
    # Act
    response = client.post(url, data={"name": "Math"}, format="json")
    # Assert
    assert response.status_code == 201
    data = response.json()
    course_id = data["id"]
    response_update = client.delete(f"{url}{course_id}/")
    assert response_update.status_code == 204
