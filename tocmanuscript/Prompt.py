class Prompt:
    """
    The Prompt class is designed to encapsulate directives, guidelines, and constraints for guiding a large language model's response. Consider the following writing tips:

    1. Target Audience, 2. Message and Theme, 3. Purpose, 4. Style and Tone, 5. Structuring and Organization, 6. Main Characters/Concepts, 7. Evidence/Background Research, and

    8. Textual Devices and Language Usage:

        Fiction:
            Metaphors and Similes: Creating vivid imagery.
            Dialogue: Revealing the character's personality.
            Foreshadowing: Building suspense.
            Alliteration and Assonance: Enhancing rhythm.
            Point of View: Controlling narration.
        Non-Fiction:
            Clarity and Precision: Ensuring understanding.
            Data Visualization: Enhancing comprehension.
            Rhetorical Questions: Engaging readers.
            Anecdotes and Case Studies: Humanizing concepts.
            Citation and Referencing: Establishing credibility.
        Both:
            Tone and Voice: Creating mood and connection.
            Active vs. Passive Voice: Controlling focus.
            Transitional Phrases: Ensuring smooth flow.

    Here's a summary of the Prompt class parameters that encapsulate all the user-given definitions:

    Directives: These are the core instructions that guide the model's response. They can include various subcategories like questions, statements, instructions, creative requests, analytical questions, hypothetical scenarios, debates, dialogues, step-by-step, and more.

    Guidelines: These shape the tone, structure, and context of the response. They can include aspects like role, style, format, context, audience awareness, cultural sensitivity, accessibility considerations, and multimodal instructions.

    Constraints: These set limitations or boundaries for the response, including length constraints, content restrictions, time, ethics, language, accessibility, legal or regulatory, domain-specific, sensitivity, and multimodal constraints.

    Example:
        guidelines = {
            'Style': 'Formal',
            'Format': 'Essay',
            'Audience Awareness': 'Academic Readers'
        }
        constraints = {
            'Length Constraints': '1000 words',
            'Content Restrictions': 'Exclude slang or colloquial language'
        }

        # Create a Prompt object for section 1
        section_1_prompt = Prompt(
            directives={'Instruction': 'Write an introduction to the topic of artificial intelligence.'},
            guidelines=guidelines,
            constraints=constraints
        )

    See more: print(Prompt.__init__.__doc__)
    """
    def __init__(self,
                 directives={},
                 guidelines={},
                 constraints={}):
        """
        Initializes the Prompt class with directives, guidelines, and constraints.

        :param directives: The core instruction that guides the model's response. Can include subcategories like:
            - Question: Asking for specific information.
            - Statement: Providing information to elicit a response.
            - Instruction: Giving a command or request.
            - QA/Debate Interaction: Structuring a question-and-answer or debate format.
            - Informational Query: Asking for factual information or explanations.
            - Creative Request: Asking the model to generate creative content like poetry, stories, etc.
            - Analytical Question: Requesting analysis, comparison, or evaluation.
            - Instructional Command: Providing step-by-step instructions or guidance.
            - Hypothetical Scenario: Posing a hypothetical situation or question.
            - Debate or Argumentation: Asking the model to take a stance or debate a topic.
            - Interactive Dialogue: Engaging in a back-and-forth dialogue or conversation.
            - Multimodal Interaction: Including non-textual elements like images, audio, etc.
            - Conditional Request: Making a request based on certain conditions or criteria.
            - Emotional Engagement: Asking the model to respond with empathy, humor, etc.
            Example:
                {
                    'Question': 'How to lose weight?',
                    ...
                }

        :param guidelines: Shapes the tone, structure, and context of the response. Can include subcategories like:
            - Role: Defining a persona or scenario.
            - Style: Guiding the language or tone.
            - Format: Specifying the structure or layout.
            - Context: Providing background information.
            - N-Shot Learning: Providing examples to guide the model's understanding.
            - Audience Awareness: Tailoring the response to a specific audience or demographic.
            - Cultural Sensitivity: Considering cultural norms, values, or customs.
            - Accessibility Considerations: Ensuring the response is accessible to all users, including those with disabilities.
            - Multimodal Instructions: Including non-textual elements or instructions, like visual, auditory, or other sensory instructions.
            Example:
                {
                    'Role': 'You are a personal trainer',
                    'Style': 'Explain in layman\'s terms',
                    ...
                }

        :param constraints: Sets limitations or boundaries for the response. Can include subcategories like:
            - Length Constraints: Limiting the response to a specific length, such as word or character count.
            - Content Restrictions: Avoiding certain words, topics, or content.
            - Time Constraints: Requiring a response within a specific time frame or historical period.
            - Ethical Constraints: Adhering to ethical guidelines, such as privacy or bias considerations.
            - Language Constraints: Specifying the language or dialect to be used.
            - Accessibility Constraints: Ensuring the content is suitable for all users, including those with disabilities.
            - Legal or Regulatory Constraints: Complying with legal or regulatory requirements.
            - Domain-Specific Constraints: Staying within a specific domain or field of knowledge.
            - Sensitivity Constraints: Avoiding content that might be considered offensive or inappropriate.
            - Multimodal Constraints: Limitations related to non-textual elements, like images or audio.
            Example:
                {
                    'Length Constraints': '100 words',
                    'Content Restrictions': 'Exclude diet, starving, heavy-weight lifting keywords',
                    ...
                }
        """
        self.directives = directives
        self.guidelines = guidelines
        self.constraints = constraints

    def __repr__(self):
        return f"Prompt(directives={self.directives}, guidelines={self.guidelines}, constraints={self.constraints})"

    def __str__(self):
        return f"Prompt(directives: {self.directives}, guidelines: {self.guidelines}, constraints: {self.constraints})"
