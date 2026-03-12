export type HourlyData = {
  hour: number;
  production: number;
};

export type DailyForecast = {
  date: string;
  hourlyData: HourlyData[];
  totalProduction: number;
  peakHour: number;
  peakProduction: number;
  solarPotentialScore: number;
  optimalWindowStart: number;
  optimalWindowEnd: number;
  optimalWindowProduction: number;
};
