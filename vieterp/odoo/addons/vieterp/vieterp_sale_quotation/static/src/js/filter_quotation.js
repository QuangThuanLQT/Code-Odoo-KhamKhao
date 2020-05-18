odoo.define('vieterp_sale_quotation.filter_quotation', function (require) {
    "use strict";

    var time = require('web.time');
    var core = require('web.core');
    var data = require('web.data');
    var session = require('web.session');
    var utils = require('web.utils');
    var Model = require('web.Model');
    var ListView = require('web.ListView');
    var datepicker = require('web.datepicker');
    var ViewManager = require('web.ViewManager')
    var _t = core._t;
    var QWeb = core.qweb;
    var FormView = require('web.FormView');
    var framework = require('web.framework');
    var crash_manager = require('web.crash_manager');

    var KanbanRecord = require('web_kanban.Record');

    KanbanRecord.include({
        renderElement: function () {
            $('.quo_search_by_range').html('')
            this._super();
            var self = this;
        },
    });

    FormView.include({
        load_record: function (record) {
            var self = this;
            $('.quo_search_by_range').html('')
            self._super.apply(self, arguments);
        },
    });

    ListView.include({

        load_list: function () {
            var self   = this;
            var result = self._super();
            if (self.last_domain) {
                if ($('.quo_search_by_range').hasClass('hidden') && $('.quo_search_by_range').length != 0 && $('.quo_search_by_range')[0].children.length == 0 ) {
                    self.render_buttons()
                  }
                $('.quo_search_by_range').removeClass('hidden')
            }
            else {
                $('.quo_search_by_range').addClass('hidden')
            }
            this.$('tfoot').css('display', 'table-header-group');
            return result;
        },

        do_search: function (domain, context, group_by) {
            var self = this;
            this.last_domain = domain;
            this.last_context = context;
            this.last_group_by = group_by;
            this.old_search = _.bind(this._super, this);
            this.tgl_search()

        },

        tgl_search: function() {
            var self = this;
            var domain = [], value, value_tmp;

            _.each(self.ts_fields, function (field) {
                value = $('.sky_item_' + field).val();

                var select_fields = $('.sky_multi_item_' + field).children('.selected'),
                    select_value = [];
                if (select_fields.length > 0) {
                    _.each(select_fields, function (item) {
                        value_tmp = $(item).data('field');
                        if (value_tmp > 0) {
                            select_value.push($(item).data('field'));
                        }
                    });
                    if (select_value.length) {
                        domain.push([field, 'in', select_value]);
                    }

                }
            });



            if (self.$search_create_uid) {
                var create_uid = self.$search_create_uid.find('.sky_create_uid').val()
                if (create_uid) {
                    domain.push(['create_uid', 'like', create_uid]);
                    var compound_domain = new data.CompoundDomain(self.last_domain, domain);
                    self.dataset.domain = compound_domain.eval();
                    return self.old_search(compound_domain, self.last_context, self.last_group_by);
                }
            }
            if (self.$search_product_id) {
                var name = self.$search_product_id.find('.sky_name').val()
                if (name) {
                    domain.push(['product_id', 'like', name]);
                    var compound_domain = new data.CompoundDomain(self.last_domain, domain);
                    self.dataset.domain = compound_domain.eval();
                    return self.old_search(compound_domain, self.last_context, self.last_group_by);
                }
            }
            if (self.$search_state && self.model == 'sale.order'){
                var state = self.$search_state.find('.sky_state').val()
                if (state) {
                    // for( var i=domain.length - 1; i>=0; i--){
                    //     if(domain[i] && (domain[i][0] === domainRemove[0]) && (domain[i][1] === domainRemove[1]) && (domain[i][2] === domainRemove[2])) {
                    //         domain.splice(i, 1);
                    //     }
                    // }
                    domain.push(['state', '=', state]);
                    // domainRemove = ['state', '=', state];
                    var compound_domain = new data.CompoundDomain(self.last_domain, domain);
                    self.dataset.domain = compound_domain.eval();
                    // checkState = false;
                    return self.old_search(compound_domain, self.last_context, self.last_group_by);
                }
            }

            this._super.apply(this, arguments);
        },

        render_buttons: function ($node) {
            var self = this;

            this._super.apply(this, arguments);
            var l10n = _t.database.parameters;
            if (this.dataset.child_name && this.dataset.child_name != null ) return false;
            self.$buttons.find('.sky-search').remove();
            $('.quo_search_by_range').html('')

            if (self.model == 'sale.order') {
                // var sky_fields = [];
                // _.each(self.columns, function (value, key, list) {
                //     if (value.string && value.string.length > 1 && value.name === "state") {
                //         sky_fields.push([value.name, value.string]);
                //     }
                // });
                // if (sky_fields.length > 0) {
                //     self.$search_state = $(QWeb.render('SkyERP.SaleState', {'sky_fields': sky_fields}))
                //     self.$search_state.find('.sky_state').on('change', function () {
                //         // checkState = true;
                //         self.tgl_search();
                //     });
                //     // self.$search_customer.appendTo($('.cl_search_by_range'));
                //     if ($('.quo_search_by_range').length > 0) {
                //         self.$search_state.appendTo($('.quo_search_by_range'));
                //     } else {
                //         setTimeout(function () {
                //             self.$search_state.appendTo($('.quo_search_by_range'));
                //         }, 1000);
                //     }
                // }
                var sky_fields = [];
                _.each(self.columns, function (value, key, list) {
                    if (value.string && value.string.length > 1 && value.name === "create_uid") {
                        sky_fields.push([value.name, value.string]);
                    }
                });
                if (sky_fields.length > 0) {
                    self.$search_create_uid = $(QWeb.render('SkyERP.Creater', {'sky_fields': sky_fields}))
                    self.$search_create_uid.find('.sky_create_uid').on('change', function () {
                        self.tgl_search();
                    });
                    // self.$search_customer.appendTo($('.cl_search_by_range'));
                    if ($('.quo_search_by_range').length > 0) {
                        self.$search_create_uid.appendTo($('.quo_search_by_range'));
                    } else {
                        setTimeout(function () {
                            self.$search_create_uid.appendTo($('.quo_search_by_range'));
                            // self.$clear_all.appendTo($('.cl_search_by_range'));
                        }, 500);
                    }
                }

                var sky_fields = [];
                _.each(self.columns, function (value, key, list) {
                    if (value.string && value.string.length > 1 && value.name === "product_id") {
                        sky_fields.push([value.name, value.string]);
                    }
                });

                if (sky_fields.length > 0) {
                    self.$search_product_id = $(QWeb.render('SkyERP.SearchName', {'sky_fields': sky_fields}))
                    self.$search_product_id.find('.sky_name').on('change', function () {
                        self.tgl_search();
                    });
                    // self.$search_customer.appendTo($('.cl_search_by_range'));
                    if ($('.quo_search_by_range').length > 0) {
                        self.$search_product_id.appendTo($('.quo_search_by_range'));
                    } else {
                        setTimeout(function () {
                            self.$search_product_id.appendTo($('.quo_search_by_range'));
                            // self.$clear_all.appendTo($('.cl_search_by_range'));
                        }, 500);
                    }
                }

                if (self.$search_create_uid || self.$search_product_id || self.$search_state) {
                    self.$clear_all = $(QWeb.render('SkyERP.ClearAll', {}))
                    $('.quo_search_by_range').on('click', '.button_clear_all', function () {
                        self.clear_tgl_search();
                    });
                    if ($('.quo_search_by_range').length > 0) {
                        setTimeout(function () {
                            self.$clear_all.appendTo($('.quo_search_by_range'));
                        }, 1000);
                    } else {
                        setTimeout(function () {
                            self.$clear_all.appendTo($('.quo_search_by_range'));
                            $('.quo_search_by_range').on('click', '.button_clear_all', function () {
                                self.clear_tgl_search();
                            });
                        }, 1000);
                    }
                }
            }

        },
    clear_tgl_search: function () {
            try {
                var self = this;
                var compound_domain = new data.CompoundDomain(self.last_domain, []);
                self.dataset.domain = compound_domain.eval();
                console.log("clear ----")
                return self.old_search(compound_domain, self.last_context, self.last_group_by);
            } catch (err) {
            }
        },


    });
});