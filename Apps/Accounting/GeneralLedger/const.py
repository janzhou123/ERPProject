from django.conf import settings
# coding: utf-8
ugettext = lambda s: s

# Journal Type choices.
JR_STATUS_CHOICES =  getattr(settings, 'JR_STATUS_CHOICES', ((1, ugettext('Unpost')),
                                                            (2, ugettext('Posting'))))
                                                         
GL_STATUS_CHOICES =  getattr(settings, 'GL_STATUS_CHOICES', ((1, ugettext('Open Periode')),
                                                            (2, ugettext('Close Periode'))))

# Chart Of Account.                                                            
COA_NO =  getattr(settings, 'COA_NO', ((1000, ugettext('1000 – Asset')), #Asset/Harta
                                        (1100, ugettext('1100 – Asset Lancar')),
                                         (1101, ugettext('1101 – Bank')),
                                         (1102, ugettext('1102 – Kas Kecil')),
                                         (1103, ugettext('1103 – Piutang')),
                                         (1104, ugettext('1104 – Persediaan')),
                                         (1105, ugettext('1105 – Biaya dibayar dimuka')),
                                         (1106, ugettext('1106 – Investasi')),
                                        (1200, ugettext('1200 – Asset Tetap')),
                                         (1201, ugettext('1201 – Asset Tetap')),
                                         (1202, ugettext('1202 – Penyusutan Asset Tetap')),
                                       (2000, ugettext('2000 – Kewajiban')), #Kewajiban/Hutang/Liability
                                        (2100, ugettext('2100 – Kewajiban Lancar')),
                                         (2101, ugettext('2101 – Hutang Usaha')),
                                         (2102, ugettext('2102 – Hutang Karyawan')),
                                         (2103, ugettext('2103 – Hutang Bank')),
                                         (2104, ugettext('2104 – Hutang Pajak')),
                                         (2105, ugettext('2105 – Hutang Lain-lain')),
                                        (2200, ugettext('2100 – Kewajiban Tidak Lancar')),
                                         (2201, ugettext('2100 – Kewajiban Jangka Panjang')),
                                       (3000, ugettext('3000 – Modal')), #Modal/Equity
                                        (3100, ugettext('3100 – Modal')),
                                         (3101, ugettext('3101 – Modal Negara')),
                                         (3102, ugettext('3102 – Modal Perseroan')),
                                       (4000, ugettext('4000 – Pendapatan')), #Pendapatan/Income
                                        (4100, ugettext('4100 – Pendapatan')),
                                         (4101, ugettext('4101 – Pendapatan Usaha')),
                                         (4102, ugettext('4102 – Pendapatan Lain')),
                                         (4103, ugettext('4103 – Pedapatan Atas Denda Keterlambatan Pembayaran')),
                                       (5000, ugettext('5000 – Biaya')), #Biaya/Expense
                                        (5100, ugettext('5100 – Biaya Produksi')),
                                         (5101, ugettext('5101 – Upah Buruh')),
                                         (5102, ugettext('5102 – Biaya Pabrik')),
                                         (5103, ugettext('5103 – Biaya Atas Denda Keterlambatan Pembayaran')),
                                        ))

                                                   
ACCOUNT_TYPE =  getattr(settings, 'ACCOUNT_TYPE', ((1000, ugettext('Harta')),
                                                    (2000, ugettext('Kewajiban')),
                                                    (3000, ugettext('Modal')),
                                                    (4000, ugettext('Pendapatan')),
                                                    (5000, ugettext('Biaya'))))

YEAR_STATUS =  getattr(settings, 'YEAR_STATUS', ((1, ugettext('Tahun Berjalan')),
                                                (2, ugettext('Tutup Tahun'))))

READONLY_FISCAL = getattr(settings, 'READONLY_FISCAL', [2])

PERIOD_STATUS =  getattr(settings, 'PERIOD_STATUS', ((1, ugettext('Periode Berjalan')),
                                                    (2, ugettext('Tutup Periode'))))

READONLY_PERIOD = getattr(settings, 'READONLY_PERIOD', [2])

JOURNAL_TYPE =  getattr(settings, 'JOURNAL_TYPE', ((1, ugettext('Penjualan')),
                                                    (2, ugettext('Belanja')),
                                                    (3, ugettext('Penggajian')),
                                                    (4, ugettext('Kas')),
                                                    (5, ugettext('Bank')),
                                                    (6, ugettext('Penyusutan')),
                                                    (7, ugettext('Penyesuaian')),
                                                    (8, ugettext('Pemindahan')),
                                                    (9, ugettext('Permodalan')),
                                                    (10, ugettext('Umum'))))

JOURNAL_STATUS =  getattr(settings, 'JOURNAL_STATUS', ((1, ugettext('Belum Terposting')),
                                                    (2, ugettext('Terposting'))))
