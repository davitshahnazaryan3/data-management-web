import pytest
from django.urls import reverse


def test_affiliation_str(new_affiliation):
    assert new_affiliation.__str__() == new_affiliation.name


def test_pi(new_person):
    name = f"{new_person.first_name[0]}. {new_person.last_name}: {new_person.email}"
    absolute_url = f"/people/{new_person.slug}/"
    
    print(new_person.affiliation.all())
    
    assert new_person.__str__() == name
    assert new_person.get_absolute_url() == absolute_url
