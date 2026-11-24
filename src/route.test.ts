import { test } from "node:test";
import assert from "node:assert/strict";
import { nextStop, type Stop } from "./route.ts";

const route: Stop[] = [
  { name: "Terminal", minutesFromStart: 0 },
  { name: "Pasar", minutesFromStart: 10 },
  { name: "Kampus", minutesFromStart: 25 },
];

test("returns the next stop after elapsed time", () => {
  assert.equal(nextStop(route, 5)?.name, "Pasar");
});

test("returns null after the last stop", () => {
  assert.equal(nextStop(route, 30), null);
});
