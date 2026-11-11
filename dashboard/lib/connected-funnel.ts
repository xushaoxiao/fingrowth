export const CREDIT_STAGES = {
  registered: "Registered",
  profile_completed: "Profile completed",
  kyc_passed: "KYC passed",
  bank_details_completed: "Bank details completed",
  credit_approved: "Credit approved",
} as const;

export type CreditStage = keyof typeof CREDIT_STAGES;

type Transition = {
  from: CreditStage;
  to: CreditStage;
  population: number;
  converted: number;
  not_progressed: number;
  conversion: number | null;
};

export type FunnelSource = {
  id: string;
  label: string;
  transport: "http" | "mcp";
};

export type FunnelState = {
  error: string | null;
  snapshot: {
    source: string;
    extracted_at: string;
    refreshed_at: string;
    stages: { id: CreditStage; definition: string }[];
    report: {
      data_kind: "synthetic" | "approved_aggregate";
      cohort: {
        product: string;
        market: string;
        registration_start: string;
        registration_end: string;
        observation_cutoff: string;
        timezone: string;
        completion_window_days: number;
      };
      counts: Record<CreditStage, number>;
      steps: Transition[];
      cumulative_conversion: Partial<Record<CreditStage, number | null>>;
    };
  } | null;
};
