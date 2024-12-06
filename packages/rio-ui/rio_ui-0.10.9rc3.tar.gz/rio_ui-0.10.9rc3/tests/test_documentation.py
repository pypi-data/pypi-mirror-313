import typing as t

import imy.docstrings
import pytest

import rio.docs


def _create_tests() -> None:
    for obj, docs in rio.docs.find_documented_objects().items():
        if isinstance(docs, imy.docstrings.FunctionDocs):
            test_cls = _create_function_tests(docs)
        else:
            assert isinstance(obj, type)
            test_cls = _create_class_tests(obj, docs)

        globals()[test_cls.__name__] = test_cls


def _create_function_tests(docs: imy.docstrings.FunctionDocs) -> type:
    # If the function is a decorator, there's no need to document that it takes
    # a function/class as an argument
    if (
        docs.metadata.decorator
        and len(docs.parameters) == 1
        and docs.parameters[0].name == "handler"
    ):
        parameters = []
    else:
        parameters = docs.parameters

    class Tests:  # type: ignore
        def test_summary(self) -> None:
            assert docs.summary is not None, f"{docs.name} has no summary"

        def test_details(self) -> None:
            assert docs.details is not None, f"{docs.name} has no details"

        @pytest.mark.parametrize(
            "param",
            parameters,
            ids=[param.name for param in parameters],
        )
        def test_param_description(
            self, param: imy.docstrings.FunctionParameter
        ) -> None:
            assert (
                param.description is not None
            ), f"{docs.name}.{param.name} has no description"

    Tests.__name__ = f"Test_{docs.name}"
    return Tests


def _create_class_tests(cls: type, docs: imy.docstrings.ClassDocs) -> type:
    methods = docs.functions

    methods_excluding_init = [
        func for func in methods if func.name != "__init__"
    ]

    # Components only need their constructor documented, attributes don't matter
    attributes = [] if issubclass(cls, rio.Component) else docs.attributes

    class Tests:
        def test_summary(self) -> None:
            assert docs.summary is not None, f"{cls.__name__} has no summary"

        def test_details(self) -> None:
            assert docs.details is not None, f"{cls.__name__} has no details"

        # Event and Error classes shouldn't be instantiated by the user, so make
        # sure their constructor is marked as private
        if docs.name.endswith(("Event", "Error")):

            def test_constructor_is_private(self):
                assert not any(
                    func_docs.name == "__init__" for func_docs in docs.functions
                ), f"Constructor of {docs.name} is not marked as private"

        @parametrize_with_name("attr", attributes)
        def test_attribute_description(
            self, attr: imy.docstrings.ClassField
        ) -> None:
            assert (
                attr.description is not None
            ), f"{cls.__name__}.{attr.name} has no description"

        # __init__ methods don't need a summary
        @parametrize_with_name("method", methods_excluding_init)
        def test_method_summary(
            self, method: imy.docstrings.FunctionDocs
        ) -> None:
            assert (
                method.summary is not None
            ), f"{cls.__name__}.{method.name} has no summary"

        # __init__ methods don't need details
        @parametrize_with_name("method", methods_excluding_init)
        def test_method_details(
            self, method: imy.docstrings.FunctionDocs
        ) -> None:
            assert (
                method.details is not None
            ), f"{cls.__name__}.{method.name} has no details"

        @parametrize_with_name("method", methods)
        def test_method_parameters(
            self, method: imy.docstrings.FunctionDocs
        ) -> None:
            params_without_description = [
                param.name
                for param in method.parameters[1:]
                if not param.description
            ]
            assert not params_without_description, f"These parameters have no description: {params_without_description}"

    Tests.__name__ = f"Test{docs.name}"
    return Tests


def parametrize_with_name(
    param_name: str,
    docs: t.Iterable[
        imy.docstrings.FunctionDocs
        | imy.docstrings.ClassDocs
        | imy.docstrings.ClassField
        | imy.docstrings.FunctionParameter
    ],
):
    def decorator(func):
        return pytest.mark.parametrize(
            param_name,
            docs,
            ids=[doc.name for doc in docs],
        )(func)

    return decorator


_create_tests()
