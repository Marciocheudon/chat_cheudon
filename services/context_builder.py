# services/context_builder.py
class ContextBuilder:
    def build_context(self, retrieved_data):
        context = ""
        for item in retrieved_data:
            context += f"{item['info']}\n"
        return context.strip()
