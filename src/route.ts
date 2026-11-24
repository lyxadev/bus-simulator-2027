export interface Stop {
  name: string;
  minutesFromStart: number;
}

export function nextStop(stops: Stop[], elapsedMinutes: number): Stop | null {
  for (const stop of stops) {
    if (stop.minutesFromStart >= elapsedMinutes) return stop;
  }
  return null;
}
