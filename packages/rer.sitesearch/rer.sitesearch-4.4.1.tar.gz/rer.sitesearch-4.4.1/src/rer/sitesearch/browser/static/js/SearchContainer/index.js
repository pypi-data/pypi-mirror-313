import React, { Component } from 'react';
import SearchFilters from '../SearchFilters';
import SearchResults from '../SearchResults';
import SpecificFilters from '../SpecificFilters';
import SearchContext from '../utils/searchContext';
import { getTranslationCatalog } from '../utils/i18n';
import apiFetch, { updateHistory } from '../utils/apiFetch';
import qs from 'query-string';
import debounce from 'lodash.debounce';
import DataObjectParser from 'dataobject-parser';

import PropTypes from 'prop-types';

const fixQuery = ({ params = {} }) => {
  const newParams = JSON.parse(JSON.stringify(params));
  const { SearchableText } = newParams;
  if (
    SearchableText &&
    SearchableText.length > 0 &&
    SearchableText.indexOf('*') !== SearchableText.length
  ) {
    newParams.SearchableText = `${newParams.SearchableText}*`;
  }
  return newParams;
};

// const nullState = {
//   filters: null,
//   results: [],
//   loading: false,
// };

class SearchContainer extends Component {
  constructor(props) {
    super(props);

    const requestQuery = qs.parse(window.location.search);
    let query = requestQuery
      ? DataObjectParser.transpose(requestQuery).data()
      : {};

    // fix queries
    Object.entries(query).forEach(([key, value]) => {
      if (typeof value === 'object' && value !== null) {
        if (value.list) {
          query[key] = {
            operator: 'and',
            query: Array.isArray(value.list) ? value.list : [value.list],
          };
        }
      } else if (typeof value === 'string' && key !== 'SearchableText') {
        if (value == 'true' || value == 'false') {
          query[key] = value;
        } else {
          query[key] = { query: value };
        }
      }
    });

    const { baseUrl, searchEndpoint } = this.props;
    const searchEndpointUrl = `${baseUrl}/@${searchEndpoint}`;
    const searchUrl = `${baseUrl}/@@${searchEndpoint}`;

    this.getTranslationFor = msgid => {
      const { translations } = this.state;
      return translations[msgid] || msgid;
    };
    this.doSearch = data => {
      const { facets } = this.state;
      let params = this.state.params;
      if (data && data.params) {
        params = data.params;
      }
      updateHistory({ url: searchUrl, params });

      // enable if we want allow to change b_size
      // if (!params.b_size) {
      //   params.b_size = b_size;
      // }
      apiFetch({
        url: searchEndpointUrl,
        params: fixQuery({ params, facets }),
        method: 'GET',
      }).then(({ data }) => {
        this.setState({
          filters: params,
          results: data.items,
          facets: data.facets,
          current_site: data.current_site,
          total: data.items_total,
          batching: data.batching,
          path_infos: data.path_infos,
          loading: false,
        });
      });
    };

    this.setFacets = facets => this.setState({ facets });
    this.setFilters = newFilters => {
      let filters = {};
      if (newFilters === null) {
        if (
          this.state.filters.SearchableText &&
          this.state.filters.SearchableText.length > 0
        ) {
          // do not remove SearchableText
          filters = { SearchableText: this.state.filters.SearchableText };
          this.setState({
            filters,
          });
        } else {
          this.setState({
            filters: {},
          });
        }
      } else {
        if (
          Object.keys(newFilters).length == 1 &&
          Object.keys(newFilters)[0] == 'SearchableText'
        ) {
          // we're updating SearchableText, so reset other filters
          filters = { SearchableText: newFilters.SearchableText };
        } else {
          filters = JSON.parse(JSON.stringify(this.state.filters));
          // always clean batching
          delete filters.b_start;

          Object.keys(newFilters).forEach(key => {
            const value = newFilters[key];
            if (value) {
              filters[key] = value;
            } else if (key in filters) {
              delete filters[key];
            }
          });
        }
      }

      if (!this.state.loading) this.setState({ loading: true });

      this.doSearch({ params: filters });
    };

    this.state = {
      results: [],
      total: 0,
      loading: Object.keys(query).length > 0,
      query: Object.keys(query).length > 0 ? query : null,
      b_size: 20,
      translations: {},
      filters: {
        ...query,
      },
      facets: {},
      current_site: '',
      doSearch: this.doSearch,
      setFacets: this.setFacets,
      setFilters: debounce(this.setFilters, 100),
      isMobile: window.innerWidth < 1200,
      path_infos: {},
      getTranslationFor: this.getTranslationFor,
      baseUrl,
      searchEndpoint,
    };
    this.handleResize = this.handleResize.bind(this);
  }

  handleResize() {
    this.setState({
      isMobile: window.innerWidth < 1200,
    });
  }

  componentDidMount() {
    window.addEventListener('resize', this.handleResize);
    const { query, facets, isMobile, baseUrl, searchEndpoint } = this.state;
    const fetches = [getTranslationCatalog()];
    if (query || isMobile) {
      updateHistory({
        url: `${baseUrl}/@@${searchEndpoint}`,
        params: query ? query : {},
      });

      fetches.push(
        apiFetch({
          url: `${baseUrl}/@${searchEndpoint}`,
          params: fixQuery({ params: query ? query : {}, facets }),
          method: 'GET',
        }),
      );
    }

    Promise.all(fetches).then(data => {
      let newState = { ...this.state };
      if (data[0]) {
        newState = { ...newState, translations: data[0] };
      }
      if (data[1]) {
        const searchResults = data[1].data;
        newState = {
          ...newState,
          results: searchResults.items || [],
          facets: searchResults.facets || {},
          current_site: searchResults.current_site || '',
          total: searchResults.items_total || 0,
          path_infos: searchResults.path_infos || {},
          batching: searchResults.batching,
          loading: false,
        };
      } else {
        newState = { ...newState, loading: false };
      }
      this.setState(newState);
    });
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleResize);
  }

  render() {
    const { isMobile, filters, facets } = this.state;
    const showSearchContainer =
      !isMobile &&
      filters &&
      filters.group &&
      facets &&
      facets.groups &&
      facets.groups.values[filters.group] &&
      facets.groups.values[filters.group].advanced_filters;
    return (
      <div className="rer-search-container">
        <SearchContext.Provider value={this.state}>
          <div className="row" aria-live="polite">
            <div className="col col-md-4">
              <SearchFilters />
            </div>
            <div className="col col-md-8">
              {showSearchContainer && <SpecificFilters id="search-container" />}
              <SearchResults />
            </div>
          </div>
        </SearchContext.Provider>
      </div>
    );
  }
}

SearchContainer.propTypes = {
  baseUrl: PropTypes.string,
  searchEndpoint: PropTypes.string,
};

export default SearchContainer;
