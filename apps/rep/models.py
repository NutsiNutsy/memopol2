from django.db import models

class RepsContainerManager(models.Manager):
    """ Manager for models to which the MEP model has a foreign key"""
    def with_counts(self):
        """ Return the models with a count property, with the count of active Reps """
        return self.get_query_set().filter(mep__active=True).annotate(count=models.Count('mep'))


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30, unique=True)

    objects = RepsContainerManager()

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.name)

    @property
    def Reps(self):
        return self.mep_set.filter(active=True)

class Party(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = RepsContainerManager()

    def __unicode__(self):
        return self.name

    @property
    def Reps(self):
        return self.mep_set.filter(active=True)


class Group(models.Model):
    abbreviation = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    objects = RepsContainerManager()

    def __unicode__(self):
        return u"%s - %s" % (self.abbreviation, self.name)

    @property
    def Reps(self):
        return self.mep_set.filter(active=True)


class Delegation(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = RepsContainerManager()

    def __unicode__(self):
        return self.name

    @property
    def Reps(self):
        return self.mep_set.filter(active=True)


class Committe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)

    objects = RepsContainerManager()

    def __unicode__(self):
        return u"%s: %s" % (self.abbreviation, self.name)

    @property
    def Reps(self):
        return self.mep_set.filter(active=True)


class Opinion(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    url = models.URLField()

    def __unicode__(self):
        return self.title

class MEP(models.Model):
    active = models.BooleanField()
    key_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=2, choices=((u'M', u'Male'), (u'F', u'Female')))
    picture = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=255)
    ep_id = models.IntegerField()
    ep_opinions = models.URLField()
    ep_debates = models.URLField()
    ep_questions = models.URLField()
    ep_declarations = models.URLField()
    ep_reports = models.URLField()
    ep_motions = models.URLField()
    ep_webpage = models.URLField()
    bxl_building_name = models.CharField(max_length=255)
    bxl_building_abbreviation = models.CharField(max_length=255)
    bxl_office = models.CharField(max_length=255)
    bxl_fax = models.CharField(max_length=255)
    bxl_phone1 = models.CharField(max_length=255)
    bxl_phone2 = models.CharField(max_length=255)
    bxl_street = models.CharField(max_length=255)
    bxl_postcode = models.CharField(max_length=255)
    stg_building_name = models.CharField(max_length=255)
    stg_building_abbreviation = models.CharField(max_length=255)
    stg_office = models.CharField(max_length=255)
    stg_fax = models.CharField(max_length=255)
    stg_phone1 = models.CharField(max_length=255)
    stg_phone2 = models.CharField(max_length=255)
    stg_street = models.CharField(max_length=255)
    stg_postcode = models.CharField(max_length=255)
    party = models.ForeignKey(Party)
    group = models.ForeignKey(Group)
    group_role = models.CharField(max_length=63)
    country = models.ForeignKey(Country)
    delegations = models.ManyToManyField(Delegation, through='DelegationRole')
    opinions = models.ManyToManyField(Opinion, through='OpinionMEP')
    committes = models.ManyToManyField(Committe, through='CommitteRole')

    def __unicode__(self):
        return self.full_name

    class Meta:
        abstract = True
        ordering = ['last_name']

class Email(models.Model):
    email = models.EmailField()
    mep = models.ForeignKey(MEP)

    def __unicode__(self):
        return self.email

class CV(models.Model):
    title = models.CharField(max_length=1023)
    mep = models.ForeignKey(MEP)

    def __unicode__(self):
        return self.title

class WebSite(models.Model):
    url = models.URLField()
    mep = models.ForeignKey(MEP)

    def __unicode__(self):
        return self.url

class DelegationRole(models.Model):
    mep = models.ForeignKey(MEP)
    delegation = models.ForeignKey(Delegation)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.mep.full_name, self.delegation)

class CommitteRole(models.Model):
    mep = models.ForeignKey(MEP)
    committe = models.ForeignKey(Committe)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.committe.abbreviation, self.mep.full_name)

class OpinionMEP(models.Model):
    mep = models.ForeignKey(MEP)
    opinion = models.ForeignKey(Opinion)
    date = models.DateField()

    def __unicode__(self):
        return u"%s : %s" % (self.opinion, self.mep)
