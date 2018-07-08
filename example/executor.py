if __name__ == "__main__":
    """
    e.g. python3 example/executor.py pipeline.java JavaExecutor '{"repo_url":"https://github.com/wayofthepie/sample-app"}'
    """
    import sys
    import importlib
    from pipeline.model import PipelineMetadata

    pipeline_module = sys.argv[1]
    pipeline_name = sys.argv[2]
    metadata = PipelineMetadata(sys.argv[3])

    Pipeline = getattr(importlib.import_module(
        pipeline_module), pipeline_name)
    pipeline = Pipeline()

    pipeline.execute(metadata)
