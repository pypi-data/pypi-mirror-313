from .jsonl import JSONLinesPathSerializer, TDMSerializer

serializers = {
    'default': lambda: JSONLinesPathSerializer(TDMSerializer())
}
