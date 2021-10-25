/* Show wikidata keywords
*/
this.ckan.module('show-wikidata', function ($, _) {
  return {
    options: {
      labels: $('#wikidata_labels ul li'),
      filter_labels: $('.filtered'),
      nav_item_labels: $('div[data-module="show-wikidata"] .nav-item a span'),
      language: $('html').attr('lang').replaceAll('_', '-').toLowerCase(),
    },
    initialize: function() {
      $.proxyAll(this, /_on/);
      // zh-tw hack
      if(this.options.language == 'zh-hant-tw') {
        this.options.language = 'zh-tw';
      }
      this.search_wikidata(this.options.nav_item_labels);
      this.search_wikidata(this.options.filter_labels);
      this.search_wikidata(this.options.labels);
    },
    search_wikidata: function(labels) {
      var language = this.options.language;
      $(labels).each(function (i, l) {
        var label = $(l).text();
        // For CKAN <= 2.7
        if (!$(l).attr('class')) {
          var split_label = label.match(/[A-Za-z0-9]+/g);
          label = split_label[0];
        }
        var url = wdk.getEntities({
          ids: label.trim()
        });
        $.get(url, function(entities) {
          if (entities.entities) {
            $.each(entities.entities, function() {
              var new_label = this.labels[language] || this.labels['zh-hant'] || this.labels.zh || this.labels.en;
              new_label = new_label.value;
              // For CKAN <= 2.7
              if (!$(l).attr('class')) {
                new_label = new_label + ' (' + split_label[1] + ')';
              }
              if($(l).is('span')) { 
                var inner = $(l).find('a');
                $(l).text(new_label);
                if (inner) {
                  $(l).append(inner);
                }
              }
              if($(l).is('li')) {
                $(l).removeClass('tag').html($("<a>", { class: 'tag', href: 'https://www.wikidata.org/wiki/' + this.id, target: '_blank' }).text(new_label));
              }
            });
          }
        });
      });
    }
  };
});
