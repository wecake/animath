from app.llm import generate_animation

class TemplateFactory:
    @staticmethod
    def generate(question):
        return generate_animation(question)