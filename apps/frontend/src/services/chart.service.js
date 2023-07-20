import http from "./http-common";

const get = (url) => {
  return http.get(`${url}`, { responseType: 'arraybuffer' })
};

const chartService = {
  get
};

export default chartService;