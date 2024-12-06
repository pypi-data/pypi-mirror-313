# auto-generated content

SORT_CONFIG = {
    'Actor': {
        'index': {
            'order': '00',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'firstName': {
            'order': '05',
            'type': 'string'
        },
        'lastName': {
            'order': '06',
            'type': 'string'
        },
        'orcid': {
            'order': '07',
            'type': 'string'
        },
        'scopusID': {
            'order': '08',
            'type': 'string'
        },
        'primaryInstitution': {
            'order': '09',
            'type': 'string'
        },
        'city': {
            'order': '10',
            'type': 'string'
        },
        'country': {
            'order': '11',
            'type': 'Term'
        },
        'email': {
            'order': '12',
            'type': 'string'
        },
        'website': {
            'order': '13',
            'type': 'any'
        },
        'dataPrivate': {
            'order': '14',
            'type': 'boolean'
        },
        'originalId': {
            'order': '15',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '16',
            'type': 'string'
        },
        'createdAt': {
            'order': '17',
            'type': 'Date'
        },
        'updatedAt': {
            'order': '18',
            'type': 'Date'
        }
    },
    'Animal': {
        'index': {
            'order': '01',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'animalId': {
            'order': '04',
            'type': 'string'
        },
        'term': {
            'order': '05',
            'type': 'Term'
        },
        'description': {
            'order': '06',
            'type': 'string'
        },
        'referencePeriod': {
            'order': '07',
            'type': 'string'
        },
        'value': {
            'order': '08',
            'type': 'number'
        },
        'sd': {
            'order': '09',
            'type': 'number'
        },
        'min': {
            'order': '10',
            'type': 'number'
        },
        'max': {
            'order': '11',
            'type': 'number'
        },
        'statsDefinition': {
            'order': '12',
            'type': 'string'
        },
        'observations': {
            'order': '13',
            'type': 'number'
        },
        'price': {
            'order': '14',
            'type': 'number'
        },
        'currency': {
            'order': '15',
            'type': 'string'
        },
        'methodClassification': {
            'order': '16',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '17',
            'type': 'string'
        },
        'source': {
            'order': '18',
            'type': 'Source'
        },
        'properties': {
            'order': '19',
            'type': 'Property'
        },
        'inputs': {
            'order': '20',
            'type': 'Input'
        },
        'practices': {
            'order': '21',
            'type': 'Practice'
        },
        'schemaVersion': {
            'order': '22',
            'type': 'string'
        },
        'added': {
            'order': '23',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '24',
            'type': '(string)'
        },
        'updated': {
            'order': '25',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '26',
            'type': '(string)'
        },
        'aggregated': {
            'order': '27',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '28',
            'type': '(string)'
        }
    },
    'Bibliography': {
        'index': {
            'order': '02',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'documentDOI': {
            'order': '05',
            'type': 'string'
        },
        'title': {
            'order': '06',
            'type': 'string'
        },
        'arxivID': {
            'order': '07',
            'type': 'string'
        },
        'scopus': {
            'order': '08',
            'type': 'string'
        },
        'mendeleyID': {
            'order': '09',
            'type': 'string'
        },
        'authors': {
            'order': '10',
            'type': 'Actor'
        },
        'outlet': {
            'order': '11',
            'type': 'string'
        },
        'year': {
            'order': '12',
            'type': 'number'
        },
        'volume': {
            'order': '13',
            'type': 'number'
        },
        'issue': {
            'order': '14',
            'type': 'string'
        },
        'chapter': {
            'order': '15',
            'type': 'string'
        },
        'pages': {
            'order': '16',
            'type': 'string'
        },
        'publisher': {
            'order': '17',
            'type': 'string'
        },
        'city': {
            'order': '18',
            'type': 'string'
        },
        'editors': {
            'order': '19',
            'type': 'Actor'
        },
        'institutionPub': {
            'order': '20',
            'type': 'Actor'
        },
        'websites': {
            'order': '21',
            'type': '(string)'
        },
        'articlePdf': {
            'order': '22',
            'type': 'string'
        },
        'dateAccessed': {
            'order': '23',
            'type': '(string)'
        },
        'abstract': {
            'order': '24',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '25',
            'type': 'string'
        }
    },
    'Completeness': {
        'index': {
            'order': '03',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'animalFeed': {
            'order': '04',
            'type': 'boolean'
        },
        'animalPopulation': {
            'order': '05',
            'type': 'boolean'
        },
        'cropResidue': {
            'order': '06',
            'type': 'boolean'
        },
        'electricityFuel': {
            'order': '07',
            'type': 'boolean'
        },
        'excreta': {
            'order': '08',
            'type': 'boolean'
        },
        'fertiliser': {
            'order': '09',
            'type': 'boolean'
        },
        'freshForage': {
            'order': '10',
            'type': 'boolean'
        },
        'ingredient': {
            'order': '11',
            'type': 'boolean'
        },
        'liveAnimalInput': {
            'order': '12',
            'type': 'boolean'
        },
        'material': {
            'order': '13',
            'type': 'boolean'
        },
        'operation': {
            'order': '14',
            'type': 'boolean'
        },
        'otherChemical': {
            'order': '15',
            'type': 'boolean'
        },
        'pesticideVeterinaryDrug': {
            'order': '16',
            'type': 'boolean'
        },
        'product': {
            'order': '17',
            'type': 'boolean'
        },
        'seed': {
            'order': '18',
            'type': 'boolean'
        },
        'soilAmendment': {
            'order': '19',
            'type': 'boolean'
        },
        'transport': {
            'order': '20',
            'type': 'boolean'
        },
        'waste': {
            'order': '21',
            'type': 'boolean'
        },
        'water': {
            'order': '22',
            'type': 'boolean'
        },
        'schemaVersion': {
            'order': '23',
            'type': 'string'
        },
        'added': {
            'order': '24',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '25',
            'type': '(string)'
        },
        'updated': {
            'order': '26',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '27',
            'type': '(string)'
        }
    },
    'Cycle': {
        'index': {
            'order': '04',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'functionalUnit': {
            'order': '06',
            'type': 'string'
        },
        'functionalUnitDetails': {
            'order': '07',
            'type': 'string'
        },
        'endDate': {
            'order': '08',
            'type': 'string'
        },
        'startDate': {
            'order': '09',
            'type': 'string'
        },
        'startDateDefinition': {
            'order': '10',
            'type': 'string'
        },
        'cycleDuration': {
            'order': '11',
            'type': 'number'
        },
        'site': {
            'order': '12',
            'type': 'Site'
        },
        'otherSites': {
            'order': '13',
            'type': 'Site'
        },
        'siteDuration': {
            'order': '14',
            'type': 'number'
        },
        'otherSitesDuration': {
            'order': '15',
            'type': '(number|null)'
        },
        'siteUnusedDuration': {
            'order': '16',
            'type': 'number'
        },
        'otherSitesUnusedDuration': {
            'order': '17',
            'type': '(number|null)'
        },
        'siteArea': {
            'order': '18',
            'type': 'number'
        },
        'otherSitesArea': {
            'order': '19',
            'type': '(number|null)'
        },
        'harvestedArea': {
            'order': '20',
            'type': 'number'
        },
        'numberOfCycles': {
            'order': '21',
            'type': 'number'
        },
        'treatment': {
            'order': '22',
            'type': 'string'
        },
        'commercialPracticeTreatment': {
            'order': '23',
            'type': 'boolean'
        },
        'numberOfReplications': {
            'order': '24',
            'type': 'number'
        },
        'sampleWeight': {
            'order': '25',
            'type': 'number'
        },
        'defaultMethodClassification': {
            'order': '26',
            'type': 'string'
        },
        'defaultMethodClassificationDescription': {
            'order': '27',
            'type': 'string'
        },
        'defaultSource': {
            'order': '28',
            'type': 'Source'
        },
        'completeness': {
            'order': '29',
            'type': 'Completeness'
        },
        'practices': {
            'order': '30',
            'type': 'Practice'
        },
        'animals': {
            'order': '31',
            'type': 'Animal'
        },
        'inputs': {
            'order': '32',
            'type': 'Input'
        },
        'products': {
            'order': '33',
            'type': 'Product'
        },
        'transformations': {
            'order': '34',
            'type': 'Transformation'
        },
        'emissions': {
            'order': '35',
            'type': 'Emission'
        },
        'dataPrivate': {
            'order': '36',
            'type': 'boolean'
        },
        'originalId': {
            'order': '37',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '38',
            'type': 'string'
        },
        'added': {
            'order': '39',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '40',
            'type': '(string)'
        },
        'updated': {
            'order': '41',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '42',
            'type': '(string)'
        },
        'aggregated': {
            'order': '43',
            'type': 'boolean'
        },
        'aggregatedDataValidated': {
            'order': '44',
            'type': 'boolean'
        },
        'aggregatedVersion': {
            'order': '45',
            'type': 'string'
        },
        'aggregatedQualityScore': {
            'order': '46',
            'type': 'number'
        },
        'aggregatedQualityScoreMax': {
            'order': '47',
            'type': 'number'
        },
        'aggregatedCycles': {
            'order': '48',
            'type': 'Cycle'
        },
        'aggregatedSources': {
            'order': '49',
            'type': 'Source'
        },
        'createdAt': {
            'order': '50',
            'type': 'Date'
        },
        'updatedAt': {
            'order': '51',
            'type': 'Date'
        }
    },
    'Emission': {
        'index': {
            'order': '05',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'value': {
            'order': '06',
            'type': '(number|null)'
        },
        'sd': {
            'order': '07',
            'type': '(number|null)'
        },
        'min': {
            'order': '08',
            'type': '(number|null)'
        },
        'max': {
            'order': '09',
            'type': '(number|null)'
        },
        'statsDefinition': {
            'order': '10',
            'type': 'string'
        },
        'observations': {
            'order': '11',
            'type': '(number|null)'
        },
        'dates': {
            'order': '12',
            'type': '(string)'
        },
        'startDate': {
            'order': '13',
            'type': 'string'
        },
        'endDate': {
            'order': '14',
            'type': 'string'
        },
        'emissionDuration': {
            'order': '15',
            'type': 'number'
        },
        'depth': {
            'order': '16',
            'type': 'number'
        },
        'methodTier': {
            'order': '17',
            'type': 'string'
        },
        'methodModel': {
            'order': '18',
            'type': 'Term'
        },
        'methodModelDescription': {
            'order': '19',
            'type': 'string'
        },
        'properties': {
            'order': '20',
            'type': 'Property'
        },
        'inputs': {
            'order': '21',
            'type': 'Term'
        },
        'animals': {
            'order': '22',
            'type': 'Term'
        },
        'transport': {
            'order': '23',
            'type': 'Term'
        },
        'operation': {
            'order': '24',
            'type': 'Term'
        },
        'transformation': {
            'order': '25',
            'type': 'Term'
        },
        'site': {
            'order': '26',
            'type': 'Site'
        },
        'source': {
            'order': '27',
            'type': 'Source'
        },
        'schemaVersion': {
            'order': '28',
            'type': 'string'
        },
        'added': {
            'order': '29',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '30',
            'type': '(string)'
        },
        'updated': {
            'order': '31',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '32',
            'type': '(string)'
        },
        'aggregated': {
            'order': '33',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '34',
            'type': '(string)'
        },
        'deleted': {
            'order': '35',
            'type': 'boolean'
        }
    },
    'ImpactAssessment': {
        'index': {
            'order': '06',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'version': {
            'order': '05',
            'type': 'string'
        },
        'versionDetails': {
            'order': '06',
            'type': 'string'
        },
        'cycle': {
            'order': '07',
            'type': 'Cycle'
        },
        'product': {
            'order': '08',
            'type': 'Product'
        },
        'functionalUnitQuantity': {
            'order': '09',
            'type': 'number'
        },
        'allocationMethod': {
            'order': '10',
            'type': 'string'
        },
        'endDate': {
            'order': '11',
            'type': 'string'
        },
        'startDate': {
            'order': '12',
            'type': 'string'
        },
        'site': {
            'order': '13',
            'type': 'Site'
        },
        'country': {
            'order': '14',
            'type': 'Term'
        },
        'region': {
            'order': '15',
            'type': 'Term'
        },
        'organisation': {
            'order': '16',
            'type': 'Organisation'
        },
        'source': {
            'order': '17',
            'type': 'Source'
        },
        'emissionsResourceUse': {
            'order': '18',
            'type': 'Indicator'
        },
        'impacts': {
            'order': '19',
            'type': 'Indicator'
        },
        'endpoints': {
            'order': '20',
            'type': 'Indicator'
        },
        'dataPrivate': {
            'order': '21',
            'type': 'boolean'
        },
        'organic': {
            'order': '22',
            'type': 'boolean'
        },
        'irrigated': {
            'order': '23',
            'type': 'boolean'
        },
        'autoGenerated': {
            'order': '24',
            'type': 'boolean'
        },
        'originalId': {
            'order': '25',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '26',
            'type': 'string'
        },
        'added': {
            'order': '27',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '28',
            'type': '(string)'
        },
        'updated': {
            'order': '29',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '30',
            'type': '(string)'
        },
        'aggregated': {
            'order': '31',
            'type': 'boolean'
        },
        'aggregatedDataValidated': {
            'order': '32',
            'type': 'boolean'
        },
        'aggregatedVersion': {
            'order': '33',
            'type': 'string'
        },
        'aggregatedQualityScore': {
            'order': '34',
            'type': 'number'
        },
        'aggregatedQualityScoreMax': {
            'order': '35',
            'type': 'number'
        },
        'aggregatedImpactAssessments': {
            'order': '36',
            'type': 'ImpactAssessment'
        },
        'aggregatedSources': {
            'order': '37',
            'type': 'Source'
        },
        'createdAt': {
            'order': '38',
            'type': 'Date'
        },
        'updatedAt': {
            'order': '39',
            'type': 'Date'
        }
    },
    'Indicator': {
        'index': {
            'order': '07',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'value': {
            'order': '05',
            'type': 'number'
        },
        'distribution': {
            'order': '06',
            'type': '(number)'
        },
        'sd': {
            'order': '07',
            'type': 'number'
        },
        'min': {
            'order': '08',
            'type': 'number'
        },
        'max': {
            'order': '09',
            'type': 'number'
        },
        'statsDefinition': {
            'order': '10',
            'type': 'string'
        },
        'observations': {
            'order': '11',
            'type': 'number'
        },
        'methodTier': {
            'order': '12',
            'type': 'string'
        },
        'methodModel': {
            'order': '13',
            'type': 'Term'
        },
        'methodModelDescription': {
            'order': '14',
            'type': 'string'
        },
        'inputs': {
            'order': '15',
            'type': 'Term'
        },
        'operation': {
            'order': '16',
            'type': 'Term'
        },
        'landCover': {
            'order': '17',
            'type': 'Term'
        },
        'transformation': {
            'order': '18',
            'type': 'Term'
        },
        'schemaVersion': {
            'order': '19',
            'type': 'string'
        },
        'added': {
            'order': '20',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '21',
            'type': '(string)'
        },
        'updated': {
            'order': '22',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '23',
            'type': '(string)'
        },
        'aggregated': {
            'order': '24',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '25',
            'type': '(string)'
        }
    },
    'Infrastructure': {
        'index': {
            'order': '08',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'name': {
            'order': '05',
            'type': 'string'
        },
        'description': {
            'order': '06',
            'type': 'string'
        },
        'startDate': {
            'order': '07',
            'type': 'string'
        },
        'endDate': {
            'order': '08',
            'type': 'string'
        },
        'defaultLifespan': {
            'order': '09',
            'type': 'number'
        },
        'defaultLifespanHours': {
            'order': '10',
            'type': 'number'
        },
        'mass': {
            'order': '11',
            'type': 'number'
        },
        'area': {
            'order': '12',
            'type': 'number'
        },
        'ownershipStatus': {
            'order': '13',
            'type': 'string'
        },
        'methodClassification': {
            'order': '14',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '15',
            'type': 'string'
        },
        'source': {
            'order': '16',
            'type': 'Source'
        },
        'impactAssessment': {
            'order': '17',
            'type': 'ImpactAssessment'
        },
        'inputs': {
            'order': '18',
            'type': 'Input'
        },
        'transport': {
            'order': '19',
            'type': 'Transport'
        },
        'schemaVersion': {
            'order': '20',
            'type': 'string'
        }
    },
    'Input': {
        'index': {
            'order': '09',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'value': {
            'order': '06',
            'type': '(number|null)'
        },
        'sd': {
            'order': '07',
            'type': '(number|null)'
        },
        'min': {
            'order': '08',
            'type': '(number|null)'
        },
        'max': {
            'order': '09',
            'type': '(number|null)'
        },
        'statsDefinition': {
            'order': '10',
            'type': 'string'
        },
        'observations': {
            'order': '11',
            'type': '(number|null)'
        },
        'dates': {
            'order': '12',
            'type': '(string)'
        },
        'startDate': {
            'order': '13',
            'type': 'string'
        },
        'endDate': {
            'order': '14',
            'type': 'string'
        },
        'inputDuration': {
            'order': '15',
            'type': 'number'
        },
        'methodClassification': {
            'order': '16',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '17',
            'type': 'string'
        },
        'model': {
            'order': '18',
            'type': 'Term'
        },
        'modelDescription': {
            'order': '19',
            'type': 'string'
        },
        'isAnimalFeed': {
            'order': '20',
            'type': 'boolean'
        },
        'fromCycle': {
            'order': '21',
            'type': 'boolean'
        },
        'producedInCycle': {
            'order': '22',
            'type': 'boolean'
        },
        'price': {
            'order': '23',
            'type': 'number'
        },
        'priceSd': {
            'order': '24',
            'type': 'number'
        },
        'priceMin': {
            'order': '25',
            'type': 'number'
        },
        'priceMax': {
            'order': '26',
            'type': 'number'
        },
        'priceStatsDefinition': {
            'order': '27',
            'type': 'string'
        },
        'cost': {
            'order': '28',
            'type': 'number'
        },
        'costSd': {
            'order': '29',
            'type': 'number'
        },
        'costMin': {
            'order': '30',
            'type': 'number'
        },
        'costMax': {
            'order': '31',
            'type': 'number'
        },
        'costStatsDefinition': {
            'order': '32',
            'type': 'string'
        },
        'currency': {
            'order': '33',
            'type': 'string'
        },
        'lifespan': {
            'order': '34',
            'type': 'number'
        },
        'operation': {
            'order': '35',
            'type': 'Term'
        },
        'country': {
            'order': '36',
            'type': 'Term'
        },
        'region': {
            'order': '37',
            'type': 'Term'
        },
        'impactAssessment': {
            'order': '38',
            'type': 'ImpactAssessment'
        },
        'impactAssessmentIsProxy': {
            'order': '39',
            'type': 'boolean'
        },
        'site': {
            'order': '40',
            'type': 'Site'
        },
        'source': {
            'order': '41',
            'type': 'Source'
        },
        'properties': {
            'order': '42',
            'type': 'Property'
        },
        'transport': {
            'order': '43',
            'type': 'Transport'
        },
        'schemaVersion': {
            'order': '44',
            'type': 'string'
        },
        'added': {
            'order': '45',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '46',
            'type': '(string)'
        },
        'updated': {
            'order': '47',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '48',
            'type': '(string)'
        },
        'aggregated': {
            'order': '49',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '50',
            'type': '(string)'
        }
    },
    'Management': {
        'index': {
            'order': '10',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'value': {
            'order': '06',
            'type': 'number|boolean'
        },
        'startDate': {
            'order': '07',
            'type': 'string'
        },
        'endDate': {
            'order': '08',
            'type': 'string'
        },
        'methodClassification': {
            'order': '09',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '10',
            'type': 'string'
        },
        'model': {
            'order': '11',
            'type': 'Term'
        },
        'modelDescription': {
            'order': '12',
            'type': 'string'
        },
        'source': {
            'order': '13',
            'type': 'Source'
        },
        'properties': {
            'order': '14',
            'type': 'Property'
        },
        'schemaVersion': {
            'order': '15',
            'type': 'string'
        },
        'added': {
            'order': '16',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '17',
            'type': '(string)'
        },
        'updated': {
            'order': '18',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '19',
            'type': '(string)'
        }
    },
    'Measurement': {
        'index': {
            'order': '11',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'value': {
            'order': '06',
            'type': '(number|boolean|null)'
        },
        'sd': {
            'order': '07',
            'type': '(number|null)'
        },
        'min': {
            'order': '08',
            'type': '(number|null)'
        },
        'max': {
            'order': '09',
            'type': '(number|null)'
        },
        'statsDefinition': {
            'order': '10',
            'type': 'string'
        },
        'observations': {
            'order': '11',
            'type': '(number|null)'
        },
        'dates': {
            'order': '12',
            'type': '(string)'
        },
        'startDate': {
            'order': '13',
            'type': 'string'
        },
        'endDate': {
            'order': '14',
            'type': 'string'
        },
        'measurementDuration': {
            'order': '15',
            'type': 'number'
        },
        'depthUpper': {
            'order': '16',
            'type': 'number'
        },
        'depthLower': {
            'order': '17',
            'type': 'number'
        },
        'latitude': {
            'order': '18',
            'type': 'number'
        },
        'longitude': {
            'order': '19',
            'type': 'number'
        },
        'methodClassification': {
            'order': '20',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '21',
            'type': 'string'
        },
        'method': {
            'order': '22',
            'type': 'Term'
        },
        'methodDescription': {
            'order': '23',
            'type': 'string'
        },
        'source': {
            'order': '24',
            'type': 'Source'
        },
        'properties': {
            'order': '25',
            'type': 'Property'
        },
        'schemaVersion': {
            'order': '26',
            'type': 'string'
        },
        'added': {
            'order': '27',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '28',
            'type': '(string)'
        },
        'updated': {
            'order': '29',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '30',
            'type': '(string)'
        },
        'aggregated': {
            'order': '31',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '32',
            'type': '(string)'
        }
    },
    'Organisation': {
        'index': {
            'order': '12',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'boundary': {
            'order': '06',
            'type': 'object'
        },
        'boundaryArea': {
            'order': '07',
            'type': 'number'
        },
        'area': {
            'order': '08',
            'type': 'number'
        },
        'latitude': {
            'order': '09',
            'type': 'number'
        },
        'longitude': {
            'order': '10',
            'type': 'number'
        },
        'streetAddress': {
            'order': '11',
            'type': 'string'
        },
        'city': {
            'order': '12',
            'type': 'string'
        },
        'region': {
            'order': '13',
            'type': 'Term'
        },
        'country': {
            'order': '14',
            'type': 'Term'
        },
        'postOfficeBoxNumber': {
            'order': '15',
            'type': 'string'
        },
        'postalCode': {
            'order': '16',
            'type': 'string'
        },
        'website': {
            'order': '17',
            'type': 'any'
        },
        'glnNumber': {
            'order': '18',
            'type': 'string'
        },
        'startDate': {
            'order': '19',
            'type': 'string'
        },
        'endDate': {
            'order': '20',
            'type': 'string'
        },
        'infrastructure': {
            'order': '21',
            'type': 'Infrastructure'
        },
        'dataPrivate': {
            'order': '22',
            'type': 'boolean'
        },
        'originalId': {
            'order': '23',
            'type': 'string'
        },
        'uploadBy': {
            'order': '24',
            'type': 'Actor'
        },
        'schemaVersion': {
            'order': '25',
            'type': 'string'
        },
        'createdAt': {
            'order': '26',
            'type': 'Date'
        },
        'updatedAt': {
            'order': '27',
            'type': 'Date'
        }
    },
    'Practice': {
        'index': {
            'order': '13',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'key': {
            'order': '06',
            'type': 'Term'
        },
        'value': {
            'order': '07',
            'type': '(string|number|boolean|null)'
        },
        'sd': {
            'order': '08',
            'type': '(number|null)'
        },
        'min': {
            'order': '09',
            'type': '(number|null)'
        },
        'max': {
            'order': '10',
            'type': '(number|null)'
        },
        'statsDefinition': {
            'order': '11',
            'type': 'string'
        },
        'observations': {
            'order': '12',
            'type': '(number|null)'
        },
        'dates': {
            'order': '13',
            'type': '(string)'
        },
        'startDate': {
            'order': '14',
            'type': 'string'
        },
        'endDate': {
            'order': '15',
            'type': 'string'
        },
        'methodClassification': {
            'order': '16',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '17',
            'type': 'string'
        },
        'model': {
            'order': '18',
            'type': 'Term'
        },
        'modelDescription': {
            'order': '19',
            'type': 'string'
        },
        'areaPercent': {
            'order': '20',
            'type': 'number'
        },
        'price': {
            'order': '21',
            'type': 'number'
        },
        'priceSd': {
            'order': '22',
            'type': 'number'
        },
        'priceMin': {
            'order': '23',
            'type': 'number'
        },
        'priceMax': {
            'order': '24',
            'type': 'number'
        },
        'priceStatsDefinition': {
            'order': '25',
            'type': 'string'
        },
        'cost': {
            'order': '26',
            'type': 'number'
        },
        'costSd': {
            'order': '27',
            'type': 'number'
        },
        'costMin': {
            'order': '28',
            'type': 'number'
        },
        'costMax': {
            'order': '29',
            'type': 'number'
        },
        'costStatsDefinition': {
            'order': '30',
            'type': 'string'
        },
        'currency': {
            'order': '31',
            'type': 'string'
        },
        'ownershipStatus': {
            'order': '32',
            'type': 'string'
        },
        'site': {
            'order': '33',
            'type': 'Site'
        },
        'source': {
            'order': '34',
            'type': 'Source'
        },
        'properties': {
            'order': '35',
            'type': 'Property'
        },
        'schemaVersion': {
            'order': '36',
            'type': 'string'
        },
        'added': {
            'order': '37',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '38',
            'type': '(string)'
        },
        'updated': {
            'order': '39',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '40',
            'type': '(string)'
        },
        'aggregated': {
            'order': '41',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '42',
            'type': '(string)'
        }
    },
    'Product': {
        'index': {
            'order': '14',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'variety': {
            'order': '06',
            'type': 'string'
        },
        'value': {
            'order': '07',
            'type': '(number|null)'
        },
        'sd': {
            'order': '08',
            'type': '(number|null)'
        },
        'min': {
            'order': '09',
            'type': '(number|null)'
        },
        'max': {
            'order': '10',
            'type': '(number|null)'
        },
        'statsDefinition': {
            'order': '11',
            'type': 'string'
        },
        'observations': {
            'order': '12',
            'type': '(number|null)'
        },
        'dates': {
            'order': '13',
            'type': '(string)'
        },
        'startDate': {
            'order': '14',
            'type': 'string'
        },
        'endDate': {
            'order': '15',
            'type': 'string'
        },
        'methodClassification': {
            'order': '16',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '17',
            'type': 'string'
        },
        'model': {
            'order': '18',
            'type': 'Term'
        },
        'modelDescription': {
            'order': '19',
            'type': 'string'
        },
        'fate': {
            'order': '20',
            'type': 'string'
        },
        'price': {
            'order': '21',
            'type': 'number'
        },
        'priceSd': {
            'order': '22',
            'type': 'number'
        },
        'priceMin': {
            'order': '23',
            'type': 'number'
        },
        'priceMax': {
            'order': '24',
            'type': 'number'
        },
        'priceStatsDefinition': {
            'order': '25',
            'type': 'string'
        },
        'revenue': {
            'order': '26',
            'type': 'number'
        },
        'revenueSd': {
            'order': '27',
            'type': 'number'
        },
        'revenueMin': {
            'order': '28',
            'type': 'number'
        },
        'revenueMax': {
            'order': '29',
            'type': 'number'
        },
        'revenueStatsDefinition': {
            'order': '30',
            'type': 'string'
        },
        'currency': {
            'order': '31',
            'type': 'string'
        },
        'economicValueShare': {
            'order': '32',
            'type': 'number'
        },
        'primary': {
            'order': '33',
            'type': 'boolean'
        },
        'source': {
            'order': '34',
            'type': 'Source'
        },
        'properties': {
            'order': '35',
            'type': 'Property'
        },
        'transport': {
            'order': '36',
            'type': 'Transport'
        },
        'schemaVersion': {
            'order': '37',
            'type': 'string'
        },
        'added': {
            'order': '38',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '39',
            'type': '(string)'
        },
        'updated': {
            'order': '40',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '41',
            'type': '(string)'
        },
        'aggregated': {
            'order': '42',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '43',
            'type': '(string)'
        }
    },
    'Property': {
        'index': {
            'order': '15',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'key': {
            'order': '06',
            'type': 'Term'
        },
        'value': {
            'order': '07',
            'type': 'number|boolean'
        },
        'share': {
            'order': '08',
            'type': 'number'
        },
        'sd': {
            'order': '09',
            'type': 'number'
        },
        'min': {
            'order': '10',
            'type': 'number'
        },
        'max': {
            'order': '11',
            'type': 'number'
        },
        'statsDefinition': {
            'order': '12',
            'type': 'string'
        },
        'observations': {
            'order': '13',
            'type': 'number'
        },
        'date': {
            'order': '14',
            'type': 'string'
        },
        'startDate': {
            'order': '15',
            'type': 'string'
        },
        'endDate': {
            'order': '16',
            'type': 'string'
        },
        'methodModel': {
            'order': '17',
            'type': 'Term'
        },
        'methodModelDescription': {
            'order': '18',
            'type': 'string'
        },
        'methodClassification': {
            'order': '19',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '20',
            'type': 'string'
        },
        'source': {
            'order': '21',
            'type': 'Source'
        },
        'dataState': {
            'order': '22',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '23',
            'type': 'string'
        },
        'added': {
            'order': '24',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '25',
            'type': '(string)'
        },
        'updated': {
            'order': '26',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '27',
            'type': '(string)'
        },
        'aggregated': {
            'order': '28',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '29',
            'type': '(string)'
        }
    },
    'Site': {
        'index': {
            'order': '16',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'organisation': {
            'order': '06',
            'type': 'Organisation'
        },
        'siteType': {
            'order': '07',
            'type': 'string'
        },
        'tenure': {
            'order': '08',
            'type': 'string'
        },
        'numberOfSites': {
            'order': '09',
            'type': 'number'
        },
        'boundary': {
            'order': '10',
            'type': 'object'
        },
        'area': {
            'order': '11',
            'type': 'number'
        },
        'areaSd': {
            'order': '12',
            'type': 'number'
        },
        'areaMin': {
            'order': '13',
            'type': 'number'
        },
        'areaMax': {
            'order': '14',
            'type': 'number'
        },
        'latitude': {
            'order': '15',
            'type': 'number'
        },
        'longitude': {
            'order': '16',
            'type': 'number'
        },
        'country': {
            'order': '17',
            'type': 'Term'
        },
        'region': {
            'order': '18',
            'type': 'Term'
        },
        'glnNumber': {
            'order': '19',
            'type': 'string'
        },
        'startDate': {
            'order': '20',
            'type': 'string'
        },
        'endDate': {
            'order': '21',
            'type': 'string'
        },
        'defaultMethodClassification': {
            'order': '22',
            'type': 'string'
        },
        'defaultMethodClassificationDescription': {
            'order': '23',
            'type': 'string'
        },
        'defaultSource': {
            'order': '24',
            'type': 'Source'
        },
        'measurements': {
            'order': '25',
            'type': 'Measurement'
        },
        'management': {
            'order': '26',
            'type': 'Management'
        },
        'infrastructure': {
            'order': '27',
            'type': 'Infrastructure'
        },
        'dataPrivate': {
            'order': '28',
            'type': 'boolean'
        },
        'boundaryArea': {
            'order': '29',
            'type': 'number'
        },
        'ecoregion': {
            'order': '30',
            'type': 'string'
        },
        'awareWaterBasinId': {
            'order': '31',
            'type': 'string'
        },
        'originalId': {
            'order': '32',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '33',
            'type': 'string'
        },
        'added': {
            'order': '34',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '35',
            'type': '(string)'
        },
        'updated': {
            'order': '36',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '37',
            'type': '(string)'
        },
        'aggregated': {
            'order': '38',
            'type': 'boolean'
        },
        'aggregatedDataValidated': {
            'order': '39',
            'type': 'boolean'
        },
        'aggregatedVersion': {
            'order': '40',
            'type': 'string'
        },
        'aggregatedSites': {
            'order': '41',
            'type': 'Site'
        },
        'aggregatedSources': {
            'order': '42',
            'type': 'Source'
        },
        'createdAt': {
            'order': '43',
            'type': 'Date'
        },
        'updatedAt': {
            'order': '44',
            'type': 'Date'
        }
    },
    'Source': {
        'index': {
            'order': '17',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'bibliography': {
            'order': '05',
            'type': 'Bibliography'
        },
        'metaAnalyses': {
            'order': '06',
            'type': 'Source'
        },
        'uploadBy': {
            'order': '07',
            'type': 'Actor'
        },
        'uploadNotes': {
            'order': '08',
            'type': 'string'
        },
        'validationDate': {
            'order': '09',
            'type': 'Date'
        },
        'validationBy': {
            'order': '10',
            'type': 'Actor'
        },
        'intendedApplication': {
            'order': '11',
            'type': 'string'
        },
        'studyReasons': {
            'order': '12',
            'type': 'string'
        },
        'intendedAudience': {
            'order': '13',
            'type': 'string'
        },
        'comparativeAssertions': {
            'order': '14',
            'type': 'boolean'
        },
        'sampleDesign': {
            'order': '15',
            'type': 'Term'
        },
        'weightingMethod': {
            'order': '16',
            'type': 'string'
        },
        'experimentDesign': {
            'order': '17',
            'type': 'Term'
        },
        'originalLicense': {
            'order': '18',
            'type': 'string'
        },
        'dataPrivate': {
            'order': '19',
            'type': 'boolean'
        },
        'originalId': {
            'order': '20',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '21',
            'type': 'string'
        },
        'createdAt': {
            'order': '22',
            'type': 'Date'
        },
        'updatedAt': {
            'order': '23',
            'type': 'Date'
        }
    },
    'Term': {
        'index': {
            'order': '18',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'name': {
            'order': '04',
            'type': 'string'
        },
        'synonyms': {
            'order': '05',
            'type': '(string)'
        },
        'definition': {
            'order': '06',
            'type': 'string'
        },
        'description': {
            'order': '07',
            'type': 'string'
        },
        'units': {
            'order': '08',
            'type': 'string'
        },
        'unitsDescription': {
            'order': '09',
            'type': 'string'
        },
        'subClassOf': {
            'order': '10',
            'type': 'Term'
        },
        'defaultProperties': {
            'order': '11',
            'type': 'Property'
        },
        'casNumber': {
            'order': '12',
            'type': 'string'
        },
        'ecoinventReferenceProductId': {
            'order': '13',
            'type': 'any'
        },
        'fishstatName': {
            'order': '14',
            'type': 'string'
        },
        'hsCode': {
            'order': '15',
            'type': 'string'
        },
        'iccCode': {
            'order': '16',
            'type': 'number'
        },
        'iso31662Code': {
            'order': '17',
            'type': 'string'
        },
        'gadmFullName': {
            'order': '18',
            'type': 'string'
        },
        'gadmId': {
            'order': '19',
            'type': 'string'
        },
        'gadmLevel': {
            'order': '20',
            'type': 'number'
        },
        'gadmName': {
            'order': '21',
            'type': 'string'
        },
        'gadmCountry': {
            'order': '22',
            'type': 'string'
        },
        'gtin': {
            'order': '23',
            'type': 'string'
        },
        'canonicalSmiles': {
            'order': '24',
            'type': 'string'
        },
        'latitude': {
            'order': '25',
            'type': 'number'
        },
        'longitude': {
            'order': '26',
            'type': 'number'
        },
        'area': {
            'order': '27',
            'type': 'number'
        },
        'openLCAId': {
            'order': '28',
            'type': 'string'
        },
        'scientificName': {
            'order': '29',
            'type': 'string'
        },
        'website': {
            'order': '30',
            'type': 'any'
        },
        'agrovoc': {
            'order': '31',
            'type': 'any'
        },
        'aquastatSpeciesFactSheet': {
            'order': '32',
            'type': 'any'
        },
        'cornellBiologicalControl': {
            'order': '33',
            'type': 'any'
        },
        'ecolabelIndex': {
            'order': '34',
            'type': 'any'
        },
        'feedipedia': {
            'order': '35',
            'type': 'any'
        },
        'fishbase': {
            'order': '36',
            'type': 'any'
        },
        'pubchem': {
            'order': '37',
            'type': 'any'
        },
        'wikipedia': {
            'order': '38',
            'type': 'any'
        },
        'termType': {
            'order': '39',
            'type': 'string'
        },
        'schemaVersion': {
            'order': '40',
            'type': 'string'
        },
        'createdAt': {
            'order': '41',
            'type': 'Date'
        },
        'updatedAt': {
            'order': '42',
            'type': 'Date'
        }
    },
    'Transformation': {
        'index': {
            'order': '19',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'transformationId': {
            'order': '04',
            'type': 'string'
        },
        'term': {
            'order': '05',
            'type': 'Term'
        },
        'description': {
            'order': '06',
            'type': 'string'
        },
        'startDate': {
            'order': '07',
            'type': 'string'
        },
        'endDate': {
            'order': '08',
            'type': 'string'
        },
        'transformationDuration': {
            'order': '09',
            'type': 'number'
        },
        'previousTransformationId': {
            'order': '10',
            'type': 'string'
        },
        'transformedShare': {
            'order': '11',
            'type': 'number'
        },
        'site': {
            'order': '12',
            'type': 'Site'
        },
        'inputs': {
            'order': '13',
            'type': 'Input'
        },
        'emissions': {
            'order': '14',
            'type': 'Emission'
        },
        'products': {
            'order': '15',
            'type': 'Product'
        },
        'practices': {
            'order': '16',
            'type': 'Practice'
        },
        'schemaVersion': {
            'order': '17',
            'type': 'string'
        },
        'added': {
            'order': '18',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '19',
            'type': '(string)'
        },
        'updated': {
            'order': '20',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '21',
            'type': '(string)'
        }
    },
    'Transport': {
        'index': {
            'order': '20',
            'type': 'string'
        },
        'type': {
            'order': '00',
            'type': 'string'
        },
        '@type': {
            'order': '01',
            'type': 'string'
        },
        '@id': {
            'order': '02',
            'type': 'string'
        },
        'id': {
            'order': '03',
            'type': 'string'
        },
        'term': {
            'order': '04',
            'type': 'Term'
        },
        'description': {
            'order': '05',
            'type': 'string'
        },
        'value': {
            'order': '06',
            'type': 'number'
        },
        'sd': {
            'order': '07',
            'type': 'number'
        },
        'min': {
            'order': '08',
            'type': 'number'
        },
        'max': {
            'order': '09',
            'type': 'number'
        },
        'statsDefinition': {
            'order': '10',
            'type': 'string'
        },
        'observations': {
            'order': '11',
            'type': '(number|null)'
        },
        'distance': {
            'order': '12',
            'type': 'number'
        },
        'distanceSd': {
            'order': '13',
            'type': 'number'
        },
        'distanceMin': {
            'order': '14',
            'type': 'number'
        },
        'distanceMax': {
            'order': '15',
            'type': 'number'
        },
        'distanceStatsDefinition': {
            'order': '16',
            'type': 'string'
        },
        'distanceObservations': {
            'order': '17',
            'type': '(number|null)'
        },
        'returnLegIncluded': {
            'order': '18',
            'type': 'boolean'
        },
        'methodModel': {
            'order': '19',
            'type': 'Term'
        },
        'methodModelDescription': {
            'order': '20',
            'type': 'string'
        },
        'methodClassification': {
            'order': '21',
            'type': 'string'
        },
        'methodClassificationDescription': {
            'order': '22',
            'type': 'string'
        },
        'source': {
            'order': '23',
            'type': 'Source'
        },
        'inputs': {
            'order': '24',
            'type': 'Input'
        },
        'practices': {
            'order': '25',
            'type': 'Practice'
        },
        'emissions': {
            'order': '26',
            'type': 'Emission'
        },
        'schemaVersion': {
            'order': '27',
            'type': 'string'
        },
        'added': {
            'order': '28',
            'type': '(string)'
        },
        'addedVersion': {
            'order': '29',
            'type': '(string)'
        },
        'updated': {
            'order': '30',
            'type': '(string)'
        },
        'updatedVersion': {
            'order': '31',
            'type': '(string)'
        },
        'aggregated': {
            'order': '32',
            'type': '(string)'
        },
        'aggregatedVersion': {
            'order': '33',
            'type': '(string)'
        }
    }
}
