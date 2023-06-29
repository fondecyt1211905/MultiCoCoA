import http from "./http-common";

const getAll = (id_process) => {
  return http.get(`/results/${id_process}`);
};

const get = (id_process, name) => {
  return http.get(`/results/${id_process}/${name}`, { responseType: "blob" });
};

const resultsService = {
  getAll,
  get,
};

export default resultsService;
