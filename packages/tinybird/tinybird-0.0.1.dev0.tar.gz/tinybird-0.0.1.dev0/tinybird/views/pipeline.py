from tabulate import tabulate

from .api_pipes import APIPipeWithDataHandler


class PipeMdHandler(APIPipeWithDataHandler):
    def render_data(self, pipe):
        self.set_header("content-type", "text/plain")
        doc = []
        doc.append(f"# {pipe.name}")
        for x in pipe.pipeline.nodes:
            doc.append(f"### {x.name}")
            if x.description:
                doc.append(f"{x.description}")
            doc.append(f"```sql\n{x.sql}\n```")
            r = x.result
            if r["error"]:
                doc.append(f"```{str(r['error'])}```" "")
            else:
                doc.append(tabulate(r["data"]["data"], headers="keys", tablefmt="github", floatfmt=".2f"))
        doc.append("\n\n\nGenerated with Tinybird, [create your own](https://tinybird.co)")
        return self.write("\n".join(doc))


class PipeStaticHtmlHandler(APIPipeWithDataHandler):
    """
    renders a pipe with the data in a HTML doc
    """

    def render_data(self, pipe):
        self.render("pipe_static.html", pipe=pipe)
