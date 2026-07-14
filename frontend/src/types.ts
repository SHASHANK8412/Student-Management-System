export type RoleName = 'Super Admin' | 'Principal' | 'Accountant' | 'Receptionist';

export interface AuthUser {
  id: number;
  public_id: string;
  full_name: string;
  email: string;
  phone?: string | null;
  role: RoleName;
  permissions: string[];
  is_active: boolean;
  is_verified: boolean;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
  expires_in: number;
}

export interface AuthResponse {
  tokens: TokenPair;
  user: AuthUser;
}

export interface DashboardKPI {
  total_students: number;
  active_students: number;
  total_collection: number;
  pending_fees: number;
  todays_collection: number;
  monthly_revenue: number;
  students_due_today: number;
  overdue_students: number;
}

export interface SeriesPoint {
  label: string;
  value: number;
}

export interface DashboardResponse {
  kpi: DashboardKPI;
  monthly_collection: SeriesPoint[];
  class_wise_revenue: SeriesPoint[];
  payment_trends: SeriesPoint[];
  due_distribution: SeriesPoint[];
  recent_activity: string[];
  upcoming_due_dates: string[];
}

export interface StudentRecord {
  id: number;
  public_id: string;
  admission_number: string;
  student_name: string;
  photo_url?: string | null;
  gender?: string | null;
  date_of_birth?: string | null;
  class_name: string;
  section?: string | null;
  roll_number?: string | null;
  father_name?: string | null;
  parent_name?: string | null;
  mother_name?: string | null;
  guardian_name?: string | null;
  phone?: string | null;
  aadhar_number?: string | null;
  pen_number?: string | null;
  caste?: string | null;
  sub_caste?: string | null;
  alternate_phone?: string | null;
  email?: string | null;
  address?: string | null;
  city?: string | null;
  state?: string | null;
  pin_code?: string | null;
  joining_date?: string | null;
  status: string;
  notes?: string | null;
}

export interface StudentFormValues {
  studentName: string;
  parentName: string;
  className: string;
  dateOfBirth: string;
  aadhaarNumber: string;
  penNumber: string;
  caste: string;
  subCaste: string;
  phoneNumber: string;
  totalFee: number;
  feePaid: number;
}

export interface FeeInvoiceRecord {
  id: number;
  invoice_number: string;
  student_id: number;
  due_date: string;
  total_fee: number;
  scholarship_amount: number;
  discount_amount: number;
  late_fee: number;
  amount_paid: number;
  balance_amount: number;
  status: string;
}

export interface PaymentRecord {
  id: number;
  payment_id: string;
  receipt_number: string;
  student_id: number;
  amount: number;
  payment_date: string;
  payment_mode: string;
  reference_number?: string | null;
  remarks?: string | null;
}
