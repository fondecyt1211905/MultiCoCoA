import http from "./http-common";

const getcsv = (indicator_name,id_analysis) => {
  return http.get(`/indicator-measure/${indicator_name}/${id_analysis}/csv`)
};

const IndicatorService = {
  getcsv,
};

export default IndicatorService;