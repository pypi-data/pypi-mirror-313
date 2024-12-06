import inspect
from typing import get_type_hints
import markdown2

# data loaders
from catalogue.dataset_loaders.data_csv_rankings import data_csv_rankings
from catalogue.dataset_loaders.custom_csv import data_custom_csv
from catalogue.dataset_loaders.auto_csv import data_auto_csv
from catalogue.dataset_loaders.graph import data_graph
from catalogue.dataset_loaders.images import data_images
from catalogue.dataset_loaders.image_pairs import data_image_pairs
from catalogue.dataset_loaders.graph_from_csv import data_graph_csv
from catalogue.dataset_loaders.uci_csv import data_uci

# model loaders
from catalogue.model_loaders.no_model import no_model
from catalogue.model_loaders.onnx import model_onnx
from catalogue.model_loaders.onnx_ensemble import model_onnx_ensemble
from catalogue.model_loaders.pytorch import model_torch
from catalogue.model_loaders.fair_node_ranking import model_fair_node_ranking
from catalogue.model_loaders.compute_researcher_ranking import (
    model_mitigation_ranking,
    model_normal_ranking,
)

# metrics
from catalogue.metrics.model_card import model_card
from catalogue.metrics.interactive_report import interactive_report
from catalogue.metrics.interactive_sklearn_report import interactive_sklearn_report
from catalogue.metrics.image_bias_analysis import image_bias_analysis
from catalogue.metrics.xai_analysis import facex_regions
from catalogue.metrics.xai_analysis_embeddings import facex_embeddings
from catalogue.metrics.ma_graph_connection import connection_properties
from catalogue.metrics.ranking_fairness import exposure_distance_comparison


def format_name(name):
    ret = " ".join(name.split("_")).replace("data ", "").replace("model ", "")
    ret = ret[0].upper() + ret[1:]
    return ret


name_to_runnable = dict()
parameters_to_class = dict()


def register(catalogue: dict, component, compatible=None):
    component = component.python_func.__mammoth_wrapped__
    signature = inspect.signature(component)
    type_hints = get_type_hints(component)

    # find argument descriptions
    doc = ""
    args_desc = dict()
    args_options = dict()
    started_args = False
    separator_title = " "
    sep_title = separator_title
    started_options = False
    for line in component.__doc__.split("\n"):
        line = line.strip()
        if line.startswith("Options:"):
            started_options = True
        elif line.startswith("Args:"):
            started_args = True
        elif line.endswith(" args:"):
            separator_title = line[:-5].strip()
            sep_title = separator_title
            if separator_title:
                separator_title = "<br><h3>" + separator_title + "</h3>"
        elif started_options and ":" in line:
            splt = line.split(":", maxsplit=2)
            args_options[splt[0]] = [option.strip() for option in splt[1].split(",")]
        elif started_args and ":" in line:
            splt = line.split(":", maxsplit=2)
            name = format_name(splt[0]).replace(sep_title + " ", "")
            name = name[0].upper() + name[1:]
            # args_desc[splt[0]] = f"{separator_title}<i>{name} - </i> {splt[1]}"

            args_desc[splt[0]] = (
                f"""{separator_title}<button
                      type="button"
                      class="btn btn-light"
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="{ splt[1] }"
                      data-description="{ splt[1] }"
                      data-name="{ name }"
                      onclick="showDescriptionModal(this)">
                      <i class="bi bi-info-circle"></i> { name }
                    </button>"""
            )

            separator_title = ""
        else:
            doc += line + "\n"

    args = list()
    args_to_classes = dict()
    for pname, parameter in signature.parameters.items():
        arg_type = type_hints.get(pname, parameter.annotation)
        assert pname != "return"
        args_to_classes[pname] = arg_type
        arg_type = arg_type.__name__
        # if arg_type == "str" and ("path" in pname.lower() or "url" in pname.lower()):
        #    arg_type = "url"
        if parameter.default is not inspect.Parameter.empty:  # ignore kwargs
            args.append(
                [
                    pname,
                    arg_type,
                    "None" if parameter.default is None else parameter.default,
                    args_desc.get(pname, format_name(pname)),
                ]
            )
        else:
            args.append(
                [pname, arg_type, "None", args_desc.get(pname, format_name(pname))]
            )

    name = format_name(component.__name__)
    assert name not in name_to_runnable
    name_to_runnable[name] = component
    catalogue[name] = {
        "description": str(
            markdown2.markdown(
                "\n".join([line for line in doc.replace("_", " ").split("\n")]),
                extras=["tables", "fenced-code-blocks", "code-friendly"],
            )
        ).replace("\n", " "),
        "parameters": args,
        "parameter_options": args_options,
        "name": component.__name__,
        "compatible": (
            []
            if compatible is None
            else [
                format_name(c.python_func.__mammoth_wrapped__.__name__)
                for c in compatible
            ]
        ),
        "return": signature.return_annotation.__name__,
    }
    args_to_classes["return"] = signature.return_annotation
    parameters_to_class[name] = args_to_classes


dataset_loaders = dict()
model_loaders = dict()
analysis_methods = dict()

register(dataset_loaders, data_auto_csv)
register(dataset_loaders, data_uci)
register(dataset_loaders, data_custom_csv)
register(dataset_loaders, data_csv_rankings)
register(dataset_loaders, data_graph)
register(dataset_loaders, data_graph_csv)
register(dataset_loaders, data_images)
register(dataset_loaders, data_image_pairs)

register(
    model_loaders,
    no_model,
    compatible=[
        data_auto_csv,
        data_custom_csv,
        data_uci,
        data_images,
        data_graph_csv,
    ],
)
register(
    model_loaders, model_onnx, compatible=[data_auto_csv, data_custom_csv, data_uci]
)
register(
    model_loaders,
    model_onnx_ensemble,
    compatible=[data_auto_csv, data_custom_csv, data_uci],
)
register(model_loaders, model_torch, compatible=[data_images, data_image_pairs])
register(model_loaders, model_fair_node_ranking, compatible=[data_graph])
register(model_loaders, model_mitigation_ranking, compatible=[data_csv_rankings])

register(analysis_methods, model_card)
register(analysis_methods, interactive_report)
register(analysis_methods, interactive_sklearn_report)
register(analysis_methods, image_bias_analysis)
register(analysis_methods, facex_regions)
register(analysis_methods, facex_embeddings)
register(analysis_methods, connection_properties)
register(
    analysis_methods,
    exposure_distance_comparison,
    compatible=[model_mitigation_ranking],
)
