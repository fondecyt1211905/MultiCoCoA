import http from "./http-common";

const getAll = () => {
  return http.get("/analysis");
};

const get = (id) => {
  return http.get(`/analysis/${id}`)
};

const analize = data => {
  return http.post("/analysis", data);
};

const remove = id => {
  return http.delete(`/analysis/${id}`);
};

const analysisService = {
  getAll,
  get,
  analize,
  remove,
};

export default analysisService;