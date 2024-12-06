// Copy of OCB/addons/sale_stock/static/src/js/qty_at_date_widget.js
// https://github.com/OCA/OCB/blob/13.0/addons/sale_stock/static/src/js/qty_at_date_widget.js

odoo.define('gestion_editorial.SaleOrderWidget', function (require) {
    "use strict";
    
    var core = require('web.core');
    var QWeb = core.qweb;
    
    var Widget = require('web.Widget');
    var Context = require('web.Context');
    var data_manager = require('web.data_manager');
    var widget_registry = require('web.widget_registry');
    var config = require('web.config');
    
    var _t = core._t;
    var time = require('web.time');
    
    var SaleOrderWidget = Widget.extend({
        template: 'gestion_editorial.SaleOrderWidget',
        events: _.extend({}, Widget.prototype.events, {
            'click .fa-info-circle': '_onClickButton',
        }),
    
        /**
         * @override
         * @param {Widget|null} parent
         * @param {Object} params
         */
        init: function (parent, params) {
            this.data = params.data;
            this._super(parent);
        },
    
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._setPopOver();
            });
        },
    
        updateState: function (state) {
            this.$el.popover('dispose');
            var candidate = state.data[this.getParent().currentRow];
            if (candidate) {
                this.data = candidate.data;
                this.renderElement();
                this._setPopOver();
            }
        },
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
        /**
         * Set a bootstrap popover on the current SaleOrderWidget widget that display available
         * quantity.
         */
        _setPopOver: function () {
            var self = this;
            if (!this.data.scheduled_date) {
                return;
            }
            this.data.delivery_date = this.data.scheduled_date.clone().add(this.getSession().getTZOffset(this.data.scheduled_date), 'minutes').format(time.getLangDateFormat());
            // The grid view need a specific date format that could be different than
            // the user one.
            this.data.delivery_date_grid = this.data.scheduled_date.clone().add(this.getSession().getTZOffset(this.data.scheduled_date), 'minutes').format('YYYY-MM-DD');
            this.data.debug = config.isDebug();
            var $content = $(QWeb.render('gestion_editorial.SaleOrderPopOver', {
                data: this.data,
            }));
            
            var options = {
                content: $content,
                html: true,
                placement: 'left',
                title: _t('Availability'),
                trigger: 'focus',
                delay: {'show': 0, 'hide': 100 },
            };
            this.$el.popover(options);
        },
    
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        _onClickButton: function () {
            // We add the property special click on the widget link.
            // This hack allows us to trigger the popover (see _setPopOver) without
            // triggering the _onRowClicked that opens the order line form view.
            this.$el.find('.fa-info-circle').prop('special_click', true);
        },
    });
    
    widget_registry.add('sale_order_widget', SaleOrderWidget);
    
    return SaleOrderWidget;
    });
    