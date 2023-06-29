import http from "./http-common";

const play = (name) => {
    return http.get(`/player/${name}`);
};

const ActivityService = {
    play,
};

export default ActivityService;