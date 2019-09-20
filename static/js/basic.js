var DatatablesBasicBasic = {
    init: function () {
        var e;
        (e = $("#m_table_1")).DataTable({
            responsive: !0,
            dom: "<'row'<'col-sm-12'tr>>\n\t\t\t<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>",
            lengthMenu: [5, 10, 25, 50],
            pageLength: 10,
            language: {lengthMenu: "显示 _MENU_"},
            order: [[1, "desc"]],
            headerCallback: function (e, a, t, n, s) {
                e.getElementsByTagName("th")[0].innerHTML = '\n                    <label class="m-checkbox m-checkbox--single m-checkbox--solid m-checkbox--brand">\n                        <input type="checkbox" value="" class="m-group-checkable">\n                        <span></span>\n                    </label>'
            },
            columnDefs: [{
                targets: 0,
                width: "30px",
                className: "dt-right",
                orderable: !1,
                render: function (e, a, t, n) {
                    return '\n                        <label class="m-checkbox m-checkbox--single m-checkbox--solid m-checkbox--brand">\n                            <input type="checkbox" value="" class="m-checkable">\n                            <span></span>\n                        </label>'
                }
            }, {
                targets: 8, render: function (e, a, t, n) {
                    var s = {
                        'True': {title: "有效", class: " m-badge--success"},
                        'False': {title: "无效", class: " m-badge--danger"}
                    };
                    return void 0 === s[e] ? e : '<span class="m-badge ' + s[e].class + ' m-badge--wide">' + s[e].title + "</span>"
                }
            },
                {
                    targets: 9, render: function (e, a, t, n) {
                        var s = {
                            'True': {title: "是", state: "accent"},
                            'False': {title: "否", state: "danger"}
                        };
                        return void 0 === s[e] ? e : '<span class="m-badge m-badge--' + s[e].state + ' m-badge--dot"></span>&nbsp;<span class="m--font-bold m--font-' + s[e].state + '">' + s[e].title + "</span>"
                    }
                }
            ]
        }), e.on("change", ".m-group-checkable", function () {
            var e = $(this).closest("table").find("td:first-child .m-checkable"), a = $(this).is(":checked");
            $(e).each(function () {
                a ? ($(this).prop("checked", !0), $(this).closest("tr").addClass("active")) : ($(this).prop("checked", !1), $(this).closest("tr").removeClass("active"))
            })
        }), e.on("change", "tbody tr .m-checkbox", function () {
            $(this).parents("tr").toggleClass("active")
        })
    }
};
jQuery(document).ready(function () {
    DatatablesBasicBasic.init()
});

//全选的功能
function checked_all() {
    //先得到所有的checkbox 得到一组checkbox  相当于数组
    var element = ("#")
    //循环这一组checkbox让每一个checkbox选中
    for (var i = 0; i < ck.length; i++) {
        var c = ck[i];//得到一个checkbox
        c.checked = true;//true代表选中
    }
}

//全不选
function not_checked_all() {
    //先得到所有的checkbox 得到一组checkbox  相当于数组
    var ck = document.getElementsByName("ck");
    //循环这一组checkbox让每一个checkbox选中
    for (var i = 0; i < ck.length; i++) {
        var c = ck[i];//得到一个checkbox
        c.checked = false;//false代表不选
    }
}

//反选
function backcheck() {//先得到所有的checkbox
    var ck = document.getElementsByName("ck");//得到一组checkbox  相当于数组
    //循环这一组checkbox让每一个checkbox选中
    for (var i = 0; i < ck.length; i++) {
        var c = ck[i];//得到一个checkbox
        if (c.checked == true) {//如果当前的checkbox是选中的则不让其选中
            ck[i].checked = false;
        } else {
            ck[i].checked = true;
        }
    }
}

//批量删除
function alldel() {
    var f = false;
    //得到要删除的主键id
    var arr = [];//用于存要删除的选中的id值

    var ck = document.getElementsByName("ck");//得到一组checkbox  相当于数组
    //循环这一组checkbox让每一个checkbox选中
    for (var i = 0; i < ck.length; i++) {
        if (ck[i].checked == true) {//代表选中
            arr.push(ck[i].value);
            f = true;
        }
    }

    //alert(arr);
    //跳到删除的servlet里去
    if (f == true) {
        if (confirm("您确认要删除吗？"))
            location.href = "servlet/DelServlet?ids=" + arr;
    } else {
        alert("请至少选中一条进行批量删除");
    }
}