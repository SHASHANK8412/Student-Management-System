import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { ArrowRight, GraduationCap, PencilLine, Plus, Search, Trash2, Wallet } from 'lucide-react';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import toast from 'react-hot-toast';

import { createInvoice, getInvoices, updateInvoice, type FeeInvoicePayload } from '@/api/fees';
import { createStudent, deleteStudent, getStudents, updateStudent, type StudentCreatePayload, type StudentUpdatePayload } from '@/api/students';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { EmptyState } from '@/components/ui/EmptyState';
import type { FeeInvoiceRecord, StudentRecord } from '@/types';

const classOptions = ['Nursery', 'LKG', 'UKG', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];

const formSchema = z.object({
  studentName: z.string().trim().min(2, 'Student name is required'),
  parentName: z.string().trim().min(2, 'Parent name is required'),
  className: z.string().min(1, 'Class is required'),
  dateOfBirth: z.string().optional().default(''),
  aadhaarNumber: z.string().trim().regex(/^\d{12}$/, 'Aadhaar number must be exactly 12 digits'),
  penNumber: z.string().optional().default(''),
  caste: z.string().trim().min(1, 'Caste is required'),
  subCaste: z.string().trim().min(1, 'Sub caste is required'),
  phoneNumber: z.string().trim().regex(/^\d{10}$/, 'Phone number must be exactly 10 digits'),
  totalFee: z.coerce.number().min(0, 'Total fee must be at least 0'),
  feePaid: z.coerce.number().min(0, 'Fee paid must be at least 0'),
}).superRefine((values, context) => {
  if (values.feePaid > values.totalFee) {
    context.addIssue({ code: z.ZodIssueCode.custom, path: ['feePaid'], message: 'Fee paid cannot exceed total fee' });
  }
});

type FormValues = z.infer<typeof formSchema>;

const blankValues: FormValues = {
  studentName: '',
  parentName: '',
  className: '',
  dateOfBirth: '',
  aadhaarNumber: '',
  penNumber: '',
  caste: '',
  subCaste: '',
  phoneNumber: '',
  totalFee: 0,
  feePaid: 0,
};

function toInputDate(value?: string | null) {
  return value ? value.slice(0, 10) : '';
}

function normalizeOptional(value: string) {
  const trimmed = value.trim();
  return trimmed.length ? trimmed : null;
}

function generateAdmissionNumber() {
  return `ADM-${Date.now().toString().slice(-6)}${Math.floor(Math.random() * 90 + 10)}`;
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 2 }).format(value);
}

function mapStudentToForm(student: StudentRecord, invoice?: FeeInvoiceRecord | undefined): FormValues {
  return {
    studentName: student.student_name ?? '',
    parentName: student.parent_name ?? student.father_name ?? '',
    className: student.class_name ?? '',
    dateOfBirth: toInputDate(student.date_of_birth),
    aadhaarNumber: student.aadhar_number ?? '',
    penNumber: student.pen_number ?? '',
    caste: student.caste ?? '',
    subCaste: student.sub_caste ?? '',
    phoneNumber: student.phone ?? '',
    totalFee: Number(invoice?.total_fee ?? 0),
    feePaid: Number(invoice?.amount_paid ?? 0),
  };
}

export function StudentsPage() {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [selectedStudent, setSelectedStudent] = useState<StudentRecord | null>(null);
  const queryClient = useQueryClient();
  const { data, isLoading, isFetching } = useQuery({
    queryKey: ['students', search, page],
    queryFn: () => getStudents({ page, page_size: 10, search }),
  });
  const { data: feeInvoices } = useQuery({
    queryKey: ['fee-invoices'],
    queryFn: () => getInvoices({ page: 1, page_size: 100 }),
  });
  const selectedStudentInvoiceQuery = useQuery({
    queryKey: ['student-invoice', selectedStudent?.id],
    queryFn: () => getInvoices({ page: 1, page_size: 1, student_id: selectedStudent?.id ?? 0 }),
    enabled: Boolean(selectedStudent?.id),
  });

  const invoiceByStudent = useMemo(() => {
    const map = new Map<number, FeeInvoiceRecord>();
    feeInvoices?.items.forEach((invoice) => map.set(invoice.student_id, invoice));
    return map;
  }, [feeInvoices]);

  const { register, handleSubmit, reset, watch, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: blankValues,
  });

  useEffect(() => {
    if (!selectedStudent) {
      reset(blankValues);
      return;
    }
    const invoice = selectedStudentInvoiceQuery.data?.items?.[0] ?? invoiceByStudent.get(selectedStudent.id);
    reset(mapStudentToForm(selectedStudent, invoice));
  }, [blankValues, invoiceByStudent, reset, selectedStudent, selectedStudentInvoiceQuery.data]);

  const totalFee = Number(watch('totalFee') || 0);
  const feePaid = Number(watch('feePaid') || 0);
  const remainingFee = Math.max(totalFee - feePaid, 0);

  async function saveStudent(values: FormValues) {
    const admissionNumber = selectedStudent?.admission_number ?? generateAdmissionNumber();
    const studentUpdatePayload: StudentUpdatePayload = {
      student_name: values.studentName,
      parent_name: normalizeOptional(values.parentName),
      class_name: values.className,
      date_of_birth: values.dateOfBirth || null,
      aadhar_number: normalizeOptional(values.aadhaarNumber),
      pen_number: normalizeOptional(values.penNumber),
      caste: normalizeOptional(values.caste),
      sub_caste: normalizeOptional(values.subCaste),
      phone: normalizeOptional(values.phoneNumber),
      status: 'Active',
    };
    const studentCreatePayload: StudentCreatePayload = {
      admission_number: admissionNumber,
      student_name: values.studentName,
      parent_name: normalizeOptional(values.parentName),
      class_name: values.className,
      date_of_birth: values.dateOfBirth || null,
      aadhar_number: normalizeOptional(values.aadhaarNumber),
      pen_number: normalizeOptional(values.penNumber),
      caste: normalizeOptional(values.caste),
      sub_caste: normalizeOptional(values.subCaste),
      phone: normalizeOptional(values.phoneNumber),
      status: 'Active',
    };

    try {
      const student = selectedStudent
        ? await updateStudent(selectedStudent.id, studentUpdatePayload)
        : await createStudent(studentCreatePayload);

      const feePayload: FeeInvoicePayload = {
        student_id: student.id,
        due_date: new Date().toISOString().slice(0, 10),
        billing_period: student.class_name,
        total_fee: values.totalFee,
        amount_paid: values.feePaid,
        balance_amount: remainingFee,
        scholarship_amount: 0,
        discount_amount: 0,
        late_fee: 0,
        status: remainingFee === 0 ? 'Paid' : values.feePaid > 0 ? 'Partial' : 'Pending',
      };

      const existingInvoice = selectedStudentInvoiceQuery.data?.items?.[0] ?? invoiceByStudent.get(student.id);
      if (existingInvoice) {
        await updateInvoice(existingInvoice.id, feePayload);
      } else {
        await createInvoice(feePayload);
      }

      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ['students'] }),
        queryClient.invalidateQueries({ queryKey: ['fee-invoices'] }),
        queryClient.invalidateQueries({ queryKey: ['student-invoice'] }),
      ]);

      toast.success(selectedStudent ? 'Student updated' : 'Student created');
      setSelectedStudent(null);
      reset(blankValues);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to save student';
      toast.error(message);
    }
  }

  async function handleDelete(student: StudentRecord) {
    if (!window.confirm(`Delete ${student.student_name}?`)) {
      return;
    }
    try {
      await deleteStudent(student.id);
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ['students'] }),
        queryClient.invalidateQueries({ queryKey: ['fee-invoices'] }),
      ]);
      if (selectedStudent?.id === student.id) {
        setSelectedStudent(null);
        reset(blankValues);
      }
      toast.success('Student deleted');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to delete student';
      toast.error(message);
    }
  }

  function startAddStudent() {
    setSelectedStudent(null);
    reset(blankValues);
    document.getElementById('student-form')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  const studentFormTitle = selectedStudent ? 'Edit Student' : 'Student Details';
  const feeFormTitle = 'Fee Details';

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Students</h1>
          <p className="mt-2 text-sm text-slate-400">Search, filter, import, and manage student records.</p>
        </div>
        <Button type="button" onClick={startAddStudent}>
          <Plus className="h-4 w-4" />
          <span className="ml-2">Add Student</span>
        </Button>
      </div>

      <form id="student-form" className="grid gap-6 xl:grid-cols-2" onSubmit={handleSubmit(saveStudent)}>
        <Card className="space-y-5">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-sky-500/15 p-3 text-sky-300">
                <GraduationCap className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm text-slate-400">Student section</p>
                <h2 className="text-2xl font-semibold">{studentFormTitle}</h2>
              </div>
            </div>
            {selectedStudent ? <Badge tone="info">Editing</Badge> : null}
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-2 block text-sm font-medium">Student Name *</label>
              <Input {...register('studentName')} placeholder="Enter student name" />
              {errors.studentName ? <p className="mt-1 text-xs text-rose-300">{errors.studentName.message}</p> : null}
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Parent Name *</label>
              <Input {...register('parentName')} placeholder="Enter parent name" />
              {errors.parentName ? <p className="mt-1 text-xs text-rose-300">{errors.parentName.message}</p> : null}
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Class *</label>
              <select {...register('className')} className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none transition focus:border-brand-400 focus:bg-white/10">
                <option value="">Select class</option>
                {classOptions.map((className) => <option key={className} value={className}>{className}</option>)}
              </select>
              {errors.className ? <p className="mt-1 text-xs text-rose-300">{errors.className.message}</p> : null}
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Date of Birth</label>
              <Input type="date" {...register('dateOfBirth')} />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Aadhaar Number *</label>
              <Input type="text" inputMode="numeric" maxLength={12} placeholder="12-digit Aadhaar" {...register('aadhaarNumber')} />
              {errors.aadhaarNumber ? <p className="mt-1 text-xs text-rose-300">{errors.aadhaarNumber.message}</p> : null}
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">PEN Number</label>
              <Input type="text" placeholder="Optional PEN number" {...register('penNumber')} />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Caste *</label>
              <Input type="text" placeholder="Enter caste" {...register('caste')} />
              {errors.caste ? <p className="mt-1 text-xs text-rose-300">{errors.caste.message}</p> : null}
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Sub Caste *</label>
              <Input type="text" placeholder="Enter sub caste" {...register('subCaste')} />
              {errors.subCaste ? <p className="mt-1 text-xs text-rose-300">{errors.subCaste.message}</p> : null}
            </div>
            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-medium">Phone Number *</label>
              <Input type="tel" inputMode="numeric" maxLength={10} placeholder="10-digit mobile number" {...register('phoneNumber')} />
              {errors.phoneNumber ? <p className="mt-1 text-xs text-rose-300">{errors.phoneNumber.message}</p> : null}
            </div>
          </div>
        </Card>

        <Card className="space-y-5">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-emerald-500/15 p-3 text-emerald-300">
                <Wallet className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm text-slate-400">Fee section</p>
                <h2 className="text-2xl font-semibold">{feeFormTitle}</h2>
              </div>
            </div>
            <Badge tone={remainingFee === 0 ? 'success' : 'warning'}>{remainingFee === 0 ? 'Settled' : 'Pending'}</Badge>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-2 block text-sm font-medium">Student Name</label>
              <Input value={watch('studentName')} readOnly className="bg-white/8 text-white/90" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Class</label>
              <Input value={watch('className')} readOnly className="bg-white/8 text-white/90" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Total Fee (₹) *</label>
              <Input type="number" min="0" step="0.01" inputMode="decimal" placeholder="0.00" {...register('totalFee', { valueAsNumber: true })} />
              {errors.totalFee ? <p className="mt-1 text-xs text-rose-300">{errors.totalFee.message}</p> : null}
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Fee Paid (₹) *</label>
              <Input type="number" min="0" step="0.01" inputMode="decimal" placeholder="0.00" {...register('feePaid', { valueAsNumber: true })} />
              {errors.feePaid ? <p className="mt-1 text-xs text-rose-300">{errors.feePaid.message}</p> : null}
            </div>
            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-medium">Remaining Fee</label>
              <Input value={formatCurrency(remainingFee)} readOnly className="bg-white/8 text-white/90" />
            </div>
          </div>

          <div className="flex flex-col gap-3 sm:flex-row">
            <Button type="submit" className="flex-1">
              {selectedStudent ? 'Update Student' : 'Save Student'}
            </Button>
            <Button type="button" variant="secondary" className="flex-1" onClick={() => { setSelectedStudent(null); reset(blankValues); }}>
              Reset Form
            </Button>
          </div>
        </Card>
      </form>

      <Card className="flex flex-col gap-4 md:flex-row md:items-center">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-4 top-3.5 h-4 w-4 text-slate-400" />
          <Input value={search} onChange={(event) => { setSearch(event.target.value); setPage(1); }} placeholder="Search by name, parent name, admission number, Aadhar number, phone, or class" className="pl-11" />
        </div>
        <div className="text-sm text-slate-400">{isFetching ? 'Refreshing...' : data ? `${data.meta.total} records` : '0 records'}</div>
      </Card>

      {isLoading ? (
        <LoadingSkeleton className="h-96 w-full" />
      ) : data?.items.length ? (
        <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5">
          <table className="w-full text-left text-sm">
            <thead className="bg-white/5 text-slate-300">
              <tr>
                <th className="px-5 py-4 font-medium">Admission No.</th>
                <th className="px-5 py-4 font-medium">Student</th>
                <th className="px-5 py-4 font-medium">Class</th>
                <th className="px-5 py-4 font-medium">Parent / Phone</th>
                <th className="px-5 py-4 font-medium">Fee</th>
                <th className="px-5 py-4 font-medium">Status</th>
                <th className="px-5 py-4 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((student) => {
                const invoice = invoiceByStudent.get(student.id);
                const total = Number(invoice?.total_fee ?? 0);
                const paid = Number(invoice?.amount_paid ?? 0);
                const balance = Number(invoice?.balance_amount ?? Math.max(total - paid, 0));
                return (
                <tr key={student.id} className="border-t border-white/10">
                  <td className="px-5 py-4">{student.admission_number}</td>
                  <td className="px-5 py-4">
                    <div className="font-medium text-white">{student.student_name}</div>
                    <div className="text-xs text-slate-400">{student.parent_name || student.father_name || 'Parent name not set'}</div>
                  </td>
                  <td className="px-5 py-4">{student.class_name} {student.section ?? ''}</td>
                  <td className="px-5 py-4">
                    <div>{student.phone ?? '-'}</div>
                    <div className="text-xs text-slate-400">{student.aadhar_number ? `Aadhar: ${student.aadhar_number}` : 'Aadhar not set'}</div>
                  </td>
                  <td className="px-5 py-4">
                    <div className="text-white">{formatCurrency(total)}</div>
                    <div className="text-xs text-slate-400">Paid {formatCurrency(paid)} | Due {formatCurrency(balance)}</div>
                  </td>
                  <td className="px-5 py-4">
                    <Badge tone={student.status === 'Active' ? 'success' : 'neutral'}>{student.status}</Badge>
                  </td>
                  <td className="px-5 py-4 text-right">
                    <div className="flex flex-wrap items-center justify-end gap-2">
                      <Button variant="ghost" className="px-3 py-2 text-sky-300 hover:text-sky-200" onClick={() => { setSelectedStudent(student); document.getElementById('student-form')?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}>
                        <PencilLine className="h-4 w-4" />
                        <span className="ml-2">Edit</span>
                      </Button>
                      <Button variant="ghost" className="px-3 py-2 text-rose-300 hover:text-rose-200" onClick={() => { void handleDelete(student); }}>
                        <Trash2 className="h-4 w-4" />
                        <span className="ml-2">Delete</span>
                      </Button>
                      <Link to={`/students/${student.id}`} className="inline-flex items-center gap-2 rounded-2xl px-3 py-2 text-sky-300 transition hover:bg-white/5 hover:text-sky-200">
                        View <ArrowRight className="h-4 w-4" />
                      </Link>
                    </div>
                  </td>
                </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <EmptyState title="No students found" description="Try a different search term or add the first student record." actionLabel="Add Student" onAction={startAddStudent} />
      )}

      {data ? (
        <div className="flex items-center justify-between text-sm text-slate-400">
          <span>Page {data.meta.page} of {data.meta.total_pages || 1}</span>
          <div className="flex gap-2">
            <Button variant="secondary" disabled={page <= 1} onClick={() => setPage((current) => Math.max(current - 1, 1))}>Previous</Button>
            <Button variant="secondary" disabled={!data || page >= data.meta.total_pages} onClick={() => setPage((current) => current + 1)}>Next</Button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
