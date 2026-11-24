import { nextStop, type Stop } from "./route.ts";

const route: Stop[] = [
  { name: "Terminal", minutesFromStart: 0 },
  { name: "Pasar", minutesFromStart: 10 },
  { name: "Kampus", minutesFromStart: 25 },
];

const next = nextStop(route, 0);
document.body.insertAdjacentHTML("beforeend", `<p>Halte berikutnya: ${next?.name ?? "-"}</p>`);
