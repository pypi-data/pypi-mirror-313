from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple, Union


@dataclass
class TableColumn:
    name: str
    type: str
    is_subcolumn: bool = field(default=False)


@dataclass
class DescribeTable:
    columns: Dict[str, TableColumn]

    @classmethod
    def from_query_data_response(cls, data_response: List[Dict[str, Any]]) -> "DescribeTable":
        table_columns = {}

        for response in data_response:
            table_column = TableColumn(
                name=response["name"], type=response["type"], is_subcolumn=bool(response["is_subcolumn"])
            )

            table_columns.update({table_column.name: table_column})

        return cls(columns=table_columns)

    def column_from_jsonpath(self, jsonpath: List[Union[str, List[str]]]) -> Optional[Tuple[TableColumn, str]]:
        """
        From jsonpath (in format from ndjson.py::get_path) find TableColumn and selector to build SELECT query

        Visit all TableColumn following the path. Generate selector relying on visited TableColumn and its parent

        >>> describe_table = DescribeTable(columns={"foo": TableColumn(name="foo", type="String")})
        >>> describe_table.column_from_jsonpath(["foo"])
        (TableColumn(name='foo', type='String', is_subcolumn=False), '`foo`')
        >>> print(describe_table.column_from_jsonpath(["bar"]))
        None
        >>> describe_table = DescribeTable(columns={"foo.bar": TableColumn(name="foo.bar", type="String")})
        >>> describe_table.column_from_jsonpath(["foo.bar"])
        (TableColumn(name='foo.bar', type='String', is_subcolumn=False), '`foo.bar`')
        >>> describe_table = DescribeTable(columns={"product": TableColumn(name="product", type="Tuple(country String, price UInt64)"), "product.country": TableColumn(name="product.country", type="String", is_subcolumn=True), "product.price":  TableColumn(name="product.price", type="UInt64", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["product", "country"])
        (TableColumn(name='product.country', type='String', is_subcolumn=True), "tupleElement(`product`, 'country')")
        >>> describe_table = DescribeTable(columns={"product": TableColumn(name="product", type="Tuple(country Tuple(code String), price UInt64)"), "product.country": TableColumn(name="product.country", type="Tuple(code String)", is_subcolumn=True), "product.price":  TableColumn(name="product.price", type="UInt64", is_subcolumn=True), "product.country.code":  TableColumn(name="product.country.code", type="String", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["product", "country", "code"])
        (TableColumn(name='product.country.code', type='String', is_subcolumn=True), "tupleElement(tupleElement(`product`, 'country'), 'code')")
        >>> describe_table = DescribeTable(columns={"product": TableColumn(name="product", type="Map(String, Tuple(old String, new String)))"), "product.keys": TableColumn(name="product.keys", type="Array(String)", is_subcolumn=True), "product.values":  TableColumn(name="product.values", type="Array(Tuple(old String, new String))", is_subcolumn=True), "product.values.old":  TableColumn(name="product.values.old", type="Array(String)", is_subcolumn=True), "product.values.new":  TableColumn(name="product.values.new", type="Array(String)", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["product", "key1", "old"])
        (TableColumn(name='product.values.old', type='Array(String)', is_subcolumn=True), "tupleElement(`product`['key1'], 'old')")
        >>> describe_table.column_from_jsonpath(["product", "key1'", "old"])
        (TableColumn(name='product.values.old', type='Array(String)', is_subcolumn=True), "tupleElement(`product`['key1\\\\''], 'old')")
        >>> describe_table = DescribeTable(columns={"products": TableColumn(name="products", type="Array(String)")})
        >>> describe_table.column_from_jsonpath(["products", []])
        (TableColumn(name='products', type='Array(String)', is_subcolumn=False), 'arrayMap(x -> x, `products`)')
        >>> print(describe_table.column_from_jsonpath(["no_list", []]))
        None
        >>> describe_table = DescribeTable(columns={"products": TableColumn(name="products", type="Array(Tuple(country String, price UInt64))"), "products.country": TableColumn(name="products.country", type="Array(String)", is_subcolumn=True), "products.price":  TableColumn(name="products.price", type="Array(UInt64)", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["products", ['country']])
        (TableColumn(name='products.country', type='Array(String)', is_subcolumn=True), "arrayMap(x -> tupleElement(x, 'country'), `products`)")
        >>> describe_table = DescribeTable(columns={"products": TableColumn(name="products", type="Array(Map(String, UInt64))"), "products.values": TableColumn(name="products.values", type="Array(UInt64)", is_subcolumn=True), "products.keys":  TableColumn(name="products.keys", type="Array(String)", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["products", ['key1']])
        (TableColumn(name='products.values', type='Array(UInt64)', is_subcolumn=True), "arrayMap(x -> x['key1'], `products`)")
        >>> describe_table = DescribeTable(columns={"shop": TableColumn(name="shop", type="Tuple(products Array(Map(String, UInt64)))"), "shop.products": TableColumn(name="shop.products", type="Array(Map(String, UInt64)))", is_subcolumn=True), "shop.products.values": TableColumn(name="shop.products.values", type="Array(Array(UInt64))", is_subcolumn=True), "shop.products.keys":  TableColumn(name="shop.products.keys", type="Array(Array(String))", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["shop", "products", ['key1']])
        (TableColumn(name='shop.products.values', type='Array(Array(UInt64))', is_subcolumn=True), "arrayMap(x -> x['key1'], tupleElement(`shop`, 'products'))")
        >>> describe_table.column_from_jsonpath(["shop", "products", ['values']])
        (TableColumn(name='shop.products.values', type='Array(Array(UInt64))', is_subcolumn=True), "arrayMap(x -> x['values'], tupleElement(`shop`, 'products'))")
        >>> describe_table = DescribeTable(columns={"products": TableColumn(name="products", type="Array(Tuple(country String, values UInt64))"), "products.country": TableColumn(name="products.country", type="Array(String)", is_subcolumn=True), "products.values":  TableColumn(name="products.values", type="Array(UInt64)", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["products", ['values']])
        (TableColumn(name='products.values', type='Array(UInt64)', is_subcolumn=True), "arrayMap(x -> tupleElement(x, 'values'), `products`)")
        >>> describe_table = DescribeTable(columns={"products.list": TableColumn(name="products.list", type="Array(String)")})
        >>> describe_table.column_from_jsonpath(["products.list", []])
        (TableColumn(name='products.list', type='Array(String)', is_subcolumn=False), 'arrayMap(x -> x, `products.list`)')
        >>> describe_table = DescribeTable(columns={"product.record": TableColumn(name="product.record", type="Tuple(country String, price UInt64)"), "product.record.country": TableColumn(name="product.record.country", type="String", is_subcolumn=True), "product.price":  TableColumn(name="product.record.price", type="UInt64", is_subcolumn=True)})
        >>> describe_table.column_from_jsonpath(["product.record", "country"])
        (TableColumn(name='product.record.country', type='String', is_subcolumn=True), "tupleElement(`product.record`, 'country')")
        """
        # avoid circular import
        from tinybird.ch import ch_escape_string

        column: Optional[TableColumn] = None
        selector: str = ""
        parent: Optional[Literal["tuple", "map"]] = None
        array_selector: str = ""

        for subpath in jsonpath:
            if isinstance(subpath, list):
                # Only one array is allowed so keep current selector and start building new one
                # arrayMap(x -> {selector}, {array_selector})
                array_selector = selector
                selector = "x"
                if subpath == []:
                    continue
            else:
                subpath = [subpath]

            for node in subpath:
                column_path = f"{column.name}.{node}" if column else node
                if column_path not in self.columns:
                    if parent == "map":
                        assert isinstance(column, TableColumn)
                        column_path = f"{column.name}.values"
                    else:
                        return None
                column = self.columns[column_path]

                if parent == "tuple":
                    selector = f"tupleElement({selector}, {ch_escape_string(node)})"
                elif parent == "map":
                    selector += f"[{ch_escape_string(node)}]"
                else:
                    selector = f"`{node}`"
                if column.type.startswith("Tuple") or column.type.startswith("Array(Tuple"):
                    parent = "tuple"
                elif column.type.startswith("Map") or column.type.startswith("Array(Map"):
                    parent = "map"

        if array_selector:
            selector = f"arrayMap(x -> {selector}, {array_selector})"

        return (column, selector) if column else None
