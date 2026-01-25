export const toMinutes = (time) => {
  if (!time) return 0;
  const [h, m] = time.split(":").map(Number);
  return h * 60 + m;
};

export function calculateFlightDuration(departureTime, arrivalTime, days = 0) {
  const depMinutes = toMinutes(departureTime);
  const arrMinutes = toMinutes(arrivalTime);

  let duration = days * 24 * 60 + (arrMinutes - depMinutes);

  // jeśli nie podano days, a arrival < departure → lot przez północ
  if (days === 0 && duration < 0) {
    duration += 24 * 60;
  }

  return duration;
}
