odoo.define('vieterp_tour_manager.dashboard_tour', function (require) {
    "use strict";
    var core = require('web.core');
    var formats = require('web.formats');
    var Model = require('web.Model');
    var session = require('web.session');
    var ajax = require('web.ajax');
    var KanbanView = require('web_kanban.KanbanView');
    var KanbanRecord = require('web_kanban.Record');
    var ActionManager = require('web.ActionManager');
    var FormView = require('web.FormView');
    var form_widget = require('web.form_widgets');
    var QWeb = core.qweb;
    var Class = require('web.Class');

    var _t = core._t;
    var _lt = core._lt;
    var localStorage = window.localStorage;


    // localStorage.removeItem('items')

    var SaleDashboardView = KanbanView.extend({
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard text-red',
        searchview_hidden: true,//  To hide the search and filter bar
        events: {
            'click .refresh_page': 'refresh_page',
            'click .doash_edit': 'action_edit_line',
            'click .action_confirm': 'action_confirm',
            'click .action_cancel': 'action_cancel',
            'click .create_sale': 'create_sale',
            'click .action_set_draft': 'action_set_draft',
            'click .new_customer': 'action_new_customer',
            'click .action_customer': 'action_customer',
            'click .action_sale_order_tour': 'action_sale_order_tour',
            'click .action_sale_order_tour_tyc': 'action_sale_order_tour_tyc',
            'click .action_sale_order_tour_ghep': 'action_sale_order_tour_ghep',
            'click .action_sale_order_spk': 'action_sale_order_spk',
            'click .action_purchase_tour': 'action_purchase_tour',
            'click .action_purchase_tour_ghep': 'action_purchase_tour_ghep',
            'click .action_purchase_tour_tyc': 'action_purchase_tour_tyc',
            'click .action_account_invoice_sale': 'action_account_invoice_sale',
            'click .action_account_invoice_purchase': 'action_account_invoice_purchase',
            // 'click .timesheets_to_approve': 'action_timesheets_to_approve',
            // 'click .job_applications': 'action_job_applications',
            // 'click .leave_allocations': 'action_leave_allocations',
            // 'click .attendance': 'action_attendance',
            // 'click .expenses': 'action_expenses',
            // 'click #generate_payroll_pdf': function(){this.generate_payroll_pdf("bar");},
            // 'click #generate_attendance_pdf': function(){this.generate_payroll_pdf("pie")},
            // 'click .my_profile': 'action_my_profile',
        },
        init: function (parent, dataset, view_id, options) {
            this._super(parent, dataset, view_id, options);
            this.options.creatable = false;
            var uid = dataset.context.uid;
            var employee_data = true;
            var isFirefox = false;
        },
        fetch_data: function () {
            // Overwrite this function with useful data
            return $.when();
        },

        render: function () {
            var super_render = this._super;
            var self = this;
            var now = new Date();
            var day = ("0" + now.getDate()).slice(-2);
            var month = ("0" + (now.getMonth() + 1)).slice(-2);
            var today = now.getFullYear() + "-" + (month) + "-" + (day);
            // if($('.dashboard_start_date').val()){
            //     var inputEmail = $('.dashboard_start_date').val();
            //     localStorage.setItem('na', inputEmail);
            //     var storedValue = localStorage.getItem('na');
            // }else{
            //     var inputEmail = today;
            //     localStorage.setItem('na1', inputEmail);
            //     var storedValue = localStorage.getItem('na1');
            // }

            var start_date = localStorage.getItem('start_date_store');
            var end_date = localStorage.getItem('end_date_store');
            self.dashboard_start_date = start_date;
            self.dashboard_end_date = end_date;
            var hr_dashboard = QWeb.render('display_date', {
                widget: self,
            });

            super_render.call(self);
            $(hr_dashboard).prependTo(self.$el);
            setTimeout(function() {
                $(".create_sale").trigger('click');
            }, 300);
        },

        // render: function () {
        //     var super_render = this._super;
        //     var self = this;
        //     var model = new Model('tour.manager').call('get_sale_order_data').then(function (result) {
        //         self.isFirefox = typeof InstallTrigger !== 'undefined';
        //         // self.sale_data = result[0]
        //         return self.fetch_data().then(function (result) {
        //             var hr_dashboard = QWeb.render('vieterp_tour_manager.dashboard_tour', {
        //                 widget: self,
        //             });
        //             super_render.call(self);
        //             $(hr_dashboard).prependTo(self.$el);
        //             // self.graph();
        //         })
        //     });
        // },
        refresh_page: function (event) {
            console.log('refresh page');
            window.location.reload();
        },
        create_sale: function () {
            var self = this;
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var start_date_store = $('.dashboard_start_date').val();
                localStorage.setItem('start_date_store', start_date_store);
            var end_date_store = $('.dashboard_end_date').val();
                localStorage.setItem('end_date_store', end_date_store);


            var model = new Model('tour.manager').call('get_sale_order_data',[start_date,end_date]).then(function (result) {
                self.isFirefox = typeof InstallTrigger !== 'undefined';
                self.sale_data = result[0]
                return self.fetch_data().then(function (result) {
                    var hr_dashboard = QWeb.render('vieterp_tour_manager.dashboard_tour', {
                        widget: self,
                    });
                    $('.hr_dashboard_header_render').remove()
                    $(hr_dashboard).prependTo('.hr_dashboard_header');
                    // self.graph();
                })
            });
        },

        action_sale_order_tour: function (event) {
            var self = this;
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('bao.cao.tour').call('get_domain_order_tour',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Sales Orders"),
                    type: 'ir.actions.act_window',
                    res_model: "bao.cao.tour",
                    views: [[false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_sale_order_tour_ghep: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('bao.cao.tour').call('get_domain_order_tour_ghep',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Sales Orders"),
                    type: 'ir.actions.act_window',
                    res_model: "bao.cao.tour",
                    views: [[false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_sale_order_tour_tyc: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('bao.cao.tour').call('get_domain_order_tour_tyc',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Sales Orders"),
                    type: 'ir.actions.act_window',
                    res_model: "bao.cao.tour",
                    views: [[false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_sale_order_spk: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('bao.cao.tour').call('get_domain_order_spk',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Sales Orders"),
                    type: 'ir.actions.act_window',
                    res_model: "bao.cao.tour",
                    views: [[false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_purchase_tour: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('purchase.tour').call('get_domain_purchase_tour',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Điều Hành"),
                    type: 'ir.actions.act_window',
                    res_model: "purchase.tour",
                    views: [[false, 'list'], [false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_purchase_tour_ghep: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('purchase.tour').call('get_domain_purchase_tour_ghep',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Điều Hành"),
                    type: 'ir.actions.act_window',
                    res_model: "purchase.tour",
                    views: [[false, 'list'], [false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_purchase_tour_tyc: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('purchase.tour').call('get_domain_purchase_tour_tyc',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Điều Hành"),
                    type: 'ir.actions.act_window',
                    res_model: "purchase.tour",
                    views: [[false, 'list'], [false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_account_invoice_sale: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('account.invoice').call('get_domain_account_invoice_sale',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Hoá đơn bán hàng"),
                    type: 'ir.actions.act_window',
                    res_model: "account.invoice",
                    views: [[false, 'list'], [false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        action_account_invoice_purchase: function (event) {
            var self = this;
            event.stopPropagation();
            event.preventDefault();
            var start_date = $('.dashboard_start_date').val()
            var end_date = $('.dashboard_end_date').val()
            var model = new Model('account.invoice').call('get_domain_account_invoice_purchase',[start_date,end_date]).then(function (result) {
                return self.do_action({
                    name: _t("Hoá đơn mua hàng"),
                    type: 'ir.actions.act_window',
                    res_model: "account.invoice",
                    views: [[false, 'list'], [false, 'form']],
                    target: 'current',
                    context: result[1],
                    domain: result[0]
                });
            })
        },

        // Function which gives random color for charts.
        getRandomColor: function () {
            var letters = '0123456789ABCDEF'.split('');
            var color = '#';
            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        },
        // Here we are plotting bar,pie chart
        // graph: function() {
        //     var self = this
        //     var ctx = this.$el.find('#myChart')
        //     // Fills the canvas with white background
        //     Chart.plugins.register({
        //       beforeDraw: function(chartInstance) {
        //         var ctx = chartInstance.chart.ctx;
        //         ctx.fillStyle = "white";
        //         ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
        //       }
        //     });
        //     var bg_color_list = []
        //     for (var i=0;i<=12;i++){
        //         bg_color_list.push(self.getRandomColor())
        //     }
        //     var myChart = new Chart(ctx, {
        //         type: 'bar',
        //         data: {
        //             //labels: ["January","February", "March", "April", "May", "June", "July", "August", "September",
        //             // "October", "November", "December"],
        //             labels: self.employee_data.payroll_label,
        //             datasets: [{
        //                 label: 'Payroll',
        //                 data: self.employee_data.payroll_dataset,
        //                 backgroundColor: bg_color_list,
        //                 borderColor: bg_color_list,
        //                 borderWidth: 1,
        //                 pointBorderColor: 'white',
        //                 pointBackgroundColor: 'red',
        //                 pointRadius: 5,
        //                 pointHoverRadius: 10,
        //                 pointHitRadius: 30,
        //                 pointBorderWidth: 2,
        //                 pointStyle: 'rectRounded'
        //             }]
        //         },
        //         options: {
        //             scales: {
        //                 yAxes: [{
        //                     ticks: {
        //                         min: 0,
        //                         max: Math.max.apply(null,self.employee_data.payroll_dataset),
        //                         //min: 1000,
        //                         //max: 100000,
        //                         stepSize: self.employee_data.
        //                         payroll_dataset.reduce((pv,cv)=>{return pv + (parseFloat(cv)||0)},0)
        //                         /self.employee_data.payroll_dataset.length
        //                       }
        //                 }]
        //             },
        //             responsive: true,
        //             maintainAspectRatio: true,
        //             animation: {
        //                 duration: 100, // general animation time
        //             },
        //             hover: {
        //                 animationDuration: 500, // duration of animations when hovering an item
        //             },
        //             responsiveAnimationDuration: 500, // animation duration after a resize
        //             legend: {
        //                 display: true,
        //                 labels: {
        //                     fontColor: 'black'
        //                 }
        //             },
        //         },
        //     });
        //     //Pie Chart
        //     var piectx = this.$el.find('#attendanceChart');
        //     bg_color_list = []
        //     for (var i=0;i<=self.employee_data.attendance_dataset.length;i++){
        //         bg_color_list.push(self.getRandomColor())
        //     }
        //     var pieChart = new Chart(piectx, {
        //         type: 'pie',
        //         data: {
        //             datasets: [{
        //                 data: self.employee_data.attendance_dataset,
        //                 backgroundColor: bg_color_list,
        //                 label: 'Attendance Pie'
        //             }],
        //             labels:self.employee_data.attendance_labels,
        //         },
        //         options: {
        //             responsive: true
        //         }
        //     });
        //     $('#emp_details').DataTable( {
        //         dom: 'Bfrtip',
        //         buttons: [
        //             'copy', 'csv', 'excel',
        //             {
        //                 extend: 'pdf',
        //                 footer: 'true',
        //                 orientation: 'landscape',
        //                 title:'Employee Details',
        //                 text: 'PDF',
        //                 exportOptions: {
        //                     modifier: {
        //                         selected: true
        //                     }
        //                 }
        //             },
        //             {
        //                 extend: 'print',
        //                 exportOptions: {
        //                 columns: ':visible'
        //                 }
        //             },
        //         'colvis'
        //         ],
        //         columnDefs: [ {
        //             targets: -1,
        //             visible: false
        //         } ],
        //         lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        //         pageLength: 15,
        //     } );
        // },
        // generate_payroll_pdf: function(chart){
        //     if (chart == 'bar'){
        //         var canvas = document.querySelector('#myChart');
        //     }
        //     else if (chart == 'pie') {
        //         var canvas = document.querySelector('#attendanceChart');
        //     }
        //
        //     //creates image
        //     var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        //     var doc = new jsPDF('landscape');
        //     doc.setFontSize(20);
        //     doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        //     doc.save('report.pdf');
        // },
    });

    var FormView_dash = FormView.extend({
        events: {
            'click .button_cancel_order': 'action_reload_page',
        },
        action_reload_page: function () {
            console.log('Button Clicked')
        },
    });

    form_widget.WidgetButton.include({
        on_click: function () {
            this._super();
            if (this.node.attrs.custom === "do_cancel") {
                var self = this;
                var urlParams = new URLSearchParams(window.location.href);
                var action_id = urlParams.get('action');
                var model = new Model("tour.manager");
                model.call("get_action_id", [action_id]).then(function (result) {
                    console.log('refresh page');
                    // window.location.reload();
                    if (result == true) {
                        setTimeout(function () {
                            window.location.reload();
                        }, '1500');
                    }
                });
            }
        },
    });

    // View adding to the registry
    core.view_registry.add('dashboard_tour_view', SaleDashboardView);
    return SaleDashboardView

});
