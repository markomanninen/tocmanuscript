from .Schema import Schema

class ResearchSchema(Schema):

    schema = {
        'Footnote': {
            'Number': {
                'Text': 'String',
                'Page': 'Integer'
            }
        },
        'Citation': {
            'Author': {
                'Year': 'Integer',
                'Title': 'String',
                'Publication': 'String'
            }
        },
        'Reference': {
            'Type': {
                'Details': 'String'
            }
        },
        'Structure': {
            'Abstract': {'Content': 'String'},
            'Introduction': {'Content': 'String'},
            'Methods': {'Content': 'String'},
            'Results': {'Content': 'String'},
            'Discussion': {'Content': 'String'},
            'Conclusion': {'Content': 'String'}
        }
    }
    def __init__(self):
        super().__init__(self.schema)

class ExperimentalResearchSchema(ResearchSchema):
    genre_schema = {
        'Hypothesis': 'String',
        'Methodology': {
            'Variables': 'String',
            'Controls': 'String',
            'Procedure': 'String'
        },
        'Analysis': {
            'Statistical_Tests': 'String',
            'Graphs': 'String'
        }
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        plural_map = {
            'Methodology': 'Methodologies',
            'Hypothesis': 'Hypotheses',
            'Analysis': 'Analyses'
        }
        super().__init__(combined_schema, plural_map)

class LiteratureReviewSchema(ResearchSchema):
    genre_schema = {
        'Scope': 'String',
        'Theme': ['List of Strings'],
        'Methodology': {
            'Selection_Criteria': 'String',
            'Sources': 'String'
        },
        'Gap': 'String'
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        plural_map = {'Methodology': 'Methodologies'}
        super().__init__(combined_schema, plural_map)

class CaseStudySchema(ResearchSchema):
    genre_schema = {
        'Subject': 'String',
        'Context': 'String',
        'Finding': 'String',
        'Implication': 'String'
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)

class SurveyResearchSchema(ResearchSchema):
    genre_schema = {
        'Questionnaire': {
            'Questions': ['List of Strings'],
            'Options': ['List of Strings']
        },
        'Sample_Size': 'Integer',
        'Data_Collection_Method': 'String',
        'Response_Rate': 'String'
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)

class TheoreticalResearchSchema(ResearchSchema):
    genre_schema = {
        'Theory': 'String',
        'Assumption': ['List of Strings'],
        'Proposition': ['List of Strings'],
        'Implication': 'String'
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)

class QualitativeResearchSchema(ResearchSchema):
    genre_schema = {
        'Research_Question': ['List of Strings'],
        'Data_Source': 'String',
        'Data_Analysis_Method': 'String',
        'Theme': ['List of Strings']
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)

class ReviewArticleSchema(ResearchSchema):
    genre_schema = {
        'Objective': 'String',
        'Inclusion_Criteria': 'String',
        'Excluded_Study': ['List of Strings'],
        'Summary_Finding': 'String'
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        plural_map = {'Excluded_Study': 'Excluded_Studies'}
        super().__init__(combined_schema, plural_map)

class MetaAnalysisSchema(ResearchSchema):
    genre_schema = {
        'Research_Question': ['List of Strings'],
        'Included_Study': ['List of Strings'],
        'Exclusion_Criteria': 'String',
        'Overall_Finding': 'String'
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        plural_map = {'Included_Study': 'Included_Studies'}
        super().__init__(combined_schema, plural_map)

class ObservationalStudySchema(ResearchSchema):
    genre_schema = {
        'Variable': ['List of Strings'],
        'Sample': 'String',
        'Data_Collection': 'String',
        'Observation': 'String'
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)
