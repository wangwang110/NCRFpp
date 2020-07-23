from graphviz import Digraph

digraph = Digraph("中文图片")

digraph.node(name="a", label="木", color="#00CD66", style="filled", fontcolor="white", fontname="Microsoft YaHei")
digraph.node(name="b", label="火", color="#FF4500", style="filled", fontcolor="white", fontname="Microsoft YaHei")
digraph.node(name="c", label="土", color="#CD950C", style="filled", fontcolor="white", fontname="Microsoft YaHei")
digraph.node(name="d", label="金", color="#FAFAD2", style="filled", fontcolor="#999999", fontname="Microsoft YaHei")
digraph.node(name="e", label="水", color="#00BFFF", style="filled", fontcolor="white", fontname="Microsoft YaHei")

digraph.edge("a", "b", label="木生火", color="#FF6666", fontcolor="#FF6666", fontname="Microsoft YaHei")
digraph.edge("b", "c", label="火生土", color="#FF6666", fontcolor="#FF6666", fontname="Microsoft YaHei")
digraph.edge("c", "d", label="土生金", color="#FF6666", fontcolor="#FF6666", fontname="Microsoft YaHei")
digraph.edge("d", "e", label="金生水", color="#FF6666", fontcolor="#FF6666", fontname="Microsoft YaHei")
digraph.edge("e", "a", label="水生木", color="#FF6666", fontcolor="#FF6666", fontname="Microsoft YaHei")

digraph.edge("a", "c", label="木克土", color="#333333", fontcolor="#333333", fontname="Microsoft YaHei")
digraph.edge("c", "e", label="土克水", color="#333333", fontcolor="#333333", fontname="Microsoft YaHei")
digraph.edge("e", "b", label="水克火", color="#333333", fontcolor="#333333", fontname="Microsoft YaHei")
digraph.edge("b", "d", label="火克金", color="#333333", fontcolor="#333333", fontname="Microsoft YaHei")
digraph.edge("d", "a", label="金克木", color="#333333", fontcolor="#333333", fontname="Microsoft YaHei")

digraph.view()