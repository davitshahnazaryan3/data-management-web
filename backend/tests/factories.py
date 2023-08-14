import datetime
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from metadata import models as metadata_models
from taxonomySearch import models as taxonomy_models
from pytest_factoryboy import register


this_year = datetime.date.today().year
DISCIPLINE = "Test"

fake = Faker()


@register
class AffiliationFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.Affiliation
        django_get_or_create = ('name',)

    name = " ".join(fake.words(nb=2))
    country = fake.country()
    description = fake.text()
    website = fake.url()
    date_added = fake.date()
    slug = fake.slug()


@register
class PersonFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.Person

    first_name = fake.first_name()
    last_name = fake.last_name()
    slug = fake.slug()
    email = fake.email()
    address = fake.address()
    phone = fake.phone_number()
    website = fake.url()
    date_added = fake.date()
    
    @factory.post_generation
    def affiliation(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.affiliation.add(*extracted)


@register
class ExperimentalFacilityFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.ExperimentalFacility

    name = " ".join(fake.words(nb=2))
    country = fake.country()
    description = fake.text()
    date_added = fake.date()
    slug = fake.slug()


@register
class EngineeringDisciplineFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.EngineeringDiscipline
        django_get_or_create = ('discipline',)
    
    discipline = DISCIPLINE
    slug = fake.slug()


@register
class ExperimentTypeFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.ExperimentType
        django_get_or_create = ('name',)

    name = fake.word()
    slug = fake.slug()


@register
class ExperimentScaleFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.ExperimentScale
        django_get_or_create = ('name',)

    name = fake.word()
    slug = fake.slug()


@register
class LicenseFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.License
        django_get_or_create = ('name',)

    name = fake.word()
    abbreviation = fake.pystr_format(string_format='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    url = fake.url()


@register
class DatasetFactory(DjangoModelFactory):
    class Meta:
        model = metadata_models.Dataset

    experiment_title = factory.LazyFunction(lambda: " ".join([fake.word() for _ in range(3)]))
    year_of_experiment = factory.LazyFunction(lambda: fake.random_int(min=1950, max=this_year))
    publications = fake.paragraph(nb_sentences=3)
    keywords = ", ".join(fake.words(nb=3))
    doi = "aaa/bbb"
    taxonomy = factory.LazyFunction(lambda: "/".join([fake.lexify(text='???') for _ in range(3)]))
    downloads = factory.LazyFunction(lambda: fake.random_int(max=10))
    url = fake.url()

    @factory.lazy_attribute
    def experiment_description(self):
        x = ""
        for _ in range(0, 5):
            x += "\n" + fake.paragraph(nb_sentences=10) + "\n"
        return x
    
    @factory.post_generation
    def experiment_type(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.experiment_type.add(*extracted)
        
    @factory.post_generation
    def experiment_scale(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.experiment_scale.add(*extracted)

    @factory.post_generation
    def experiment_pi(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.experiment_pi.add(*extracted)
    
    @factory.post_generation
    def experiment_facility(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.experiment_facility.add(*extracted)
    
    @factory.post_generation
    def license(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.license.add(*extracted)
    

def get_abbr(text):
    if len(text) > 5:
        return text[:5].upper()
    else:
        return text.upper()


@register
class SpecimenSubTypeFactory(DjangoModelFactory):
    class Meta:
        model = taxonomy_models.SpecimenSubType
        django_get_or_create = ('long_name', 'short_name',)
    
    long_name = factory.LazyFunction(fake.word)
    short_name = factory.LazyAttribute(lambda _: get_abbr(_.long_name))


@register
class MaterialTechnologyFactory(DjangoModelFactory):
    class Meta:
        model = taxonomy_models.MaterialTechnology
        django_get_or_create = ('long_name', 'short_name',)

    long_name = factory.LazyFunction(fake.word)
    short_name = factory.LazyAttribute(lambda _: get_abbr(_.long_name))


@register
class TypeMaterialFactory(DjangoModelFactory):
    class Meta:
        model = taxonomy_models.TypeMaterial
        django_get_or_create = ('long_name', 'short_name',)

    long_name = factory.LazyFunction(fake.word)
    short_name = factory.LazyAttribute(lambda _: get_abbr(_.long_name))
    
    @factory.post_generation
    def technology(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.technology.add(*extracted)
    

@register
class SpecimenTypeFactory(DjangoModelFactory):
    class Meta:
        model = taxonomy_models.SpecimenType
        django_get_or_create = ('long_name', 'short_name',)

    # short_name = fake.pystr_format(string_format='???', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    long_name = factory.LazyFunction(fake.word)
    short_name = factory.LazyAttribute(lambda _: get_abbr(_.long_name))

    
    @factory.post_generation
    def specimen_sub_type(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.specimen_sub_type.add(*extracted)

    @factory.post_generation
    def material_type(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        self.material_type.add(*extracted)

