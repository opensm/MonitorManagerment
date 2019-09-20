var DatatablesBasicBasic = {
    init: function () {
        var e;
        (e = $("#m_table_1")).DataTable({
            responsive: !0,
            dom: "<'row'<'col-sm-12'tr>>\n\t\t\t<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>",
            lengthMenu: [5, 10, 25, 50, 100],
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
            },
            //     {
            //     targets: 8, render: function (e, a, t, n) {
            //         var s = {
            //             'True': {title: "有效", class: " m-badge--success"},
            //             'False': {title: "无效", class: " m-badge--danger"}
            //         };
            //         return void 0 === s[e] ? e : '<span class="m-badge ' + s[e].class + ' m-badge--wide">' + s[e].title + "</span>"
            //     }
            // },
            //     {
            //         targets: 9, render: function (e, a, t, n) {
            //             var s = {
            //                 'True': {title: "是", state: "accent"},
            //                 'False': {title: "否", state: "danger"}
            //             };
            //             return void 0 === s[e] ? e : '<span class="m-badge m-badge--' + s[e].state + ' m-badge--dot"></span>&nbsp;<span class="m--font-bold m--font-' + s[e].state + '">' + s[e].title + "</span>"
            //         }
            //     }
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