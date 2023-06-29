import http from "./http-common";

const getAll = () => {
  return http.get("/activities");
};

const get = (name) => {
  return http.get(`/activities/${name}`)
};

const getFile = (name) => {
    return http.get(`/activities/${name}`, {responseType: 'blob'});
};

const create = (data) => {
  return http.post("/activities", data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

const raname = (id, data) => {
  return http.put(`/activities/${id}`, data);
};

const remove = name => {
  return http.delete(`/activities/${name}`);
};

const ActivityService = {
  getAll,
  get,
  getFile,
  create,
  raname,
  remove,
};

export default ActivityService;