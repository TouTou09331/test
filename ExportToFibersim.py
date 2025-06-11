# -*- coding: utf-8 -*-

import wx
import wx.xrc
import wx.grid
import os
import pandas as pd

# 导入 wxFormBuilder 生成的界面定义
from fibersim_dialog import Fibersim_dialog


# --- 自定义 Grid 单元格渲染器类，保留以防其他需求) ---
# 此渲染器用于强制绘制指定颜色的边框。
# 如果未来没有其他需要自定义边框的情况，这个类可以完全移除。
class DataCellBorderRenderer(wx.grid.GridCellStringRenderer):
    def __init__(self, border_colour=wx.BLACK, border_width=1):
        super().__init__()
        self.border_colour = border_colour
        self.border_width = border_width

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        绘制单元格内容和自定义边框。
        此渲染器会强制绘制一个边框，即使Grid本身没有显式设置边框颜色。
        """
        # 1. 绘制背景色
        bg_colour = attr.GetBackgroundColour() if attr.HasBackgroundColour() else wx.WHITE
        dc.SetBrush(wx.Brush(bg_colour, wx.BRUSHSTYLE_SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)  # 在绘制矩形背景时，不绘制边框，避免边框重叠
        dc.DrawRectangle(rect)

        # 2. 绘制文本内容
        super().Draw(grid, attr, dc, rect, row, col, isSelected)

        # 3. 绘制自定义边框
        dc.SetPen(wx.Pen(self.border_colour, self.border_width, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)  # 边框内部不填充
        dc.DrawRectangle(rect)  # 绘制矩形边框


# --- 计算 Grid 的目标行和列数 ---
def calculate_target_dimensions(df, min_rows, min_cols):
    num_data_rows = len(df) #实际数据行数
    num_data_cols = len(df.columns) if not df.empty else 0 #实际数据列数

    target_rows = max(num_data_rows, min_rows) #取数据行数和最小行数的最大值
    target_cols = max(num_data_cols, min_cols) #取数据列数和最小列数的最大值
    return target_rows, target_cols, num_data_rows, num_data_cols


class ExportFibersim(Fibersim_dialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.bSizerGridsContent = self.m_scrolledGridPanel.GetSizer()

        # 定义 Grid 单元格显示相关的常量
        self.MIN_FONT_SIZE = 8
        self.DEFAULT_CELL_HEIGHT = 10
        self.MIN_CELL_WIDTH = 50

        # 定义 Grid 的最小显示行列数，确保即使数据为空也有默认大小
        self.GLOBAL_MIN_ROWS = 10
        self.GLOBAL_MIN_COLUMNS = 20

        # 禁用滚动条，因为将动态调整 Grid 大小，并让 Sizer 管理布局
        self.m_scrolledGridPanel.SetScrollbars(0, 0, 0, 0)
        self.m_scrolledGridPanel.EnableScrolling(False, False)

        # 收集所有 Grid 对象到一个列表中
        self.all_grids = [self.m_gridStructuralUnitID, self.m_gridPlyNumbers,
                          self.m_gridPlyRatio, self.m_gridPlyBase]

        # 对每个 Grid 进行初始化设置
        for grid_obj in self.all_grids:
            grid_obj.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            grid_obj.EnableGridLines(True)
            # 设置所有 Grid 的默认网格线颜色为浅灰色
            grid_obj.SetGridLineColour(wx.Colour(200, 200, 200))

        # self.black_border_renderer = DataCellBorderRenderer(wx.BLACK, 1)

        # m_bpButton_ShowGrid路径设置
        image_path = r"D:\wxFormBuilder_V3.9\fibersim_dialog\Pictures\import_data .png"  # <--- 已修改为您的图片路径

        if os.path.exists(image_path):
            try:
                # 加载位图
                bmp = wx.Bitmap(image_path, wx.BITMAP_TYPE_ANY)
                if bmp.IsOk():
                    # 将位图设置到按钮上
                    self.m_bpButton_ShowGrid.SetBitmapLabel(bmp)
                else:
                    print(f"Warning: Could not load bitmap from {image_path}. Check file format or corruption.")
                    self.m_bpButton_ShowGrid.SetLabel("...")
            except Exception as e:
                print(f"Error loading bitmap for m_bpButton_ShowGrid: {e}")
                self.m_bpButton_ShowGrid.SetLabel("...")
        else:
            print(f"Warning: Image file not found at {image_path}. Setting button label to '...'.")
            self.m_bpButton_ShowGrid.SetLabel("...")

        # 绑定按钮事件
        self.m_bpButton_ShowGrid.Bind(wx.EVT_BUTTON, self.OnImportDataClicked)
        self.m_buttonStartImport.Bind(wx.EVT_BUTTON, self.OnStartImportClicked)
        self.m_buttonApply.Bind(wx.EVT_BUTTON, self.OnApplyClicked)
        self.m_buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancelClicked)

        # 初始隐藏包含 Grid 的滚动面板，在加载数据后显示
        self.m_scrolledGridPanel.Hide()
        self.Layout()
        self.Fit()

    def Destroy(self):
        for grid_obj in self.all_grids:
            if grid_obj and grid_obj.GetNumberRows() > 0 and grid_obj.GetNumberCols() > 0:
                for r in range(grid_obj.GetNumberRows()):
                    for c in range(grid_obj.GetNumberCols()):
                        # 确保清除任何可能存在的自定义渲染器
                        if grid_obj.GetCellRenderer(r, c) is not None:
                            grid_obj.SetCellRenderer(r, c, None)
                grid_obj.ClearGrid()
                grid_obj.DeleteRows(0, grid_obj.GetNumberRows())
                grid_obj.DeleteCols(0, grid_obj.GetNumberCols())
                grid_obj.ForceRefresh()
                grid_obj.Update()

        super().Destroy()

    def OnImportDataClicked(self, event):

        # 定义文件过滤器，只显示 Excel 文件类型
        wildcard = "Excel files (*.xlsx;*.xls)|*.xlsx;*.xls|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "选择导入尺寸定义表", wildcard=wildcard,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.m_textCtrl_ImportGrid.SetValue(path)
            self.load_excel_data_and_populate_grids(path)

            self.m_scrolledGridPanel.Show()
            self.Layout()
            self.Fit()
        dlg.Destroy()
        event.Skip()

    def load_excel_data_and_populate_grids(self, excel_path):
        try:
            xls = pd.ExcelFile(excel_path)
            sheet_names = xls.sheet_names

            grid_sheet_map = {
                self.m_gridStructuralUnitID: '结构单元ID',
                self.m_gridPlyNumbers: '铺层数',
                self.m_gridPlyRatio: '铺层比',
                self.m_gridPlyBase: '铺层库'
            }

            all_dfs = {}
            max_cols_overall = 0
            total_ideal_content_height = 0

            for grid_obj, sheet_name in grid_sheet_map.items():
                if grid_obj.GetNumberRows() > 0 and grid_obj.GetNumberCols() > 0:
                    for r in range(grid_obj.GetNumberRows()):
                        for c in range(grid_obj.GetNumberCols()):
                            grid_obj.SetCellRenderer(r, c, None)

                if grid_obj.GetNumberRows() > 0:
                    grid_obj.DeleteRows(0, grid_obj.GetNumberRows())
                if grid_obj.GetNumberCols() > 0:
                    grid_obj.DeleteCols(0, grid_obj.GetNumberCols())

                grid_obj.SetMinSize(wx.Size(1, 1))

                df = pd.DataFrame()
                if sheet_name in sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=None, skiprows=0)
                    if not df.empty:
                        df = df.applymap(lambda x: '' if pd.isna(x) or x is None else x)
                        df = df.loc[~(df == '').all(axis=1)]
                        df = df.loc[:, ~(df == '').all(axis=0)]
                else:
                    print(f"Warning: Sheet '{sheet_name}' not found in Excel file. Populating empty grid.")

                all_dfs[grid_obj] = df

                target_rows, target_cols, num_data_rows, num_data_cols = calculate_target_dimensions(
                    df, self.GLOBAL_MIN_ROWS, self.GLOBAL_MIN_COLUMNS
                )

                max_cols_overall = max(max_cols_overall, target_cols)

                total_ideal_content_height += (target_rows * self.DEFAULT_CELL_HEIGHT) + grid_obj.GetColLabelSize() + 5

            display_area_height = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y) * 0.8

            height_scale_factor = 1.0
            if total_ideal_content_height > display_area_height and total_ideal_content_height > 0:
                height_scale_factor = display_area_height / total_ideal_content_height

            calculated_font_size = max(self.MIN_FONT_SIZE, int(8 * height_scale_factor))
            calculated_row_height = max(10, int(self.DEFAULT_CELL_HEIGHT * height_scale_factor))

            grids_to_finalize = []
            for grid_obj, df in all_dfs.items():
                is_first_grid = (grid_obj == self.m_gridStructuralUnitID)
                # --- 传入 None 作为 custom_renderer，因为我们不再需要它 ---
                self.fill_grid(grid_obj, df, calculated_font_size, calculated_row_height, is_first_grid, None)
                #在custom_renderer上加入self.black_border_renderer即可为单元格加上黑色边框
                if grid_obj.GetNumberCols() > 0:
                    grids_to_finalize.append(grid_obj)

            self.bSizerGridsContent.Layout()# 重新布局 Sizer
            self.m_scrolledGridPanel.SetVirtualSize(self.bSizerGridsContent.GetMinSize())# 设置滚动面板的虚拟大小
            self.m_scrolledGridPanel.SetMinSize(self.bSizerGridsContent.GetMinSize())# 设置滚动面板的最小尺寸
            self.m_scrolledGridPanel.Layout()# 重新布局滚动面板
            self.Layout()# 重新布局对话框
            self.Fit()# 调整对话框大小以适应内容

            # 使用 wx.CallAfter 确保在 GUI 布局完成后再调整列宽，避免在布局过程中出现问题
            wx.CallAfter(self.finalize_all_grid_column_widths, grids_to_finalize, max_cols_overall)

            # 再次调用布局和适应窗口，确保最终显示正确
            wx.CallAfter(self.Layout)
            wx.CallAfter(self.Fit)

        except Exception as e:
            raise  # 重新抛出异常，让 OnImportDataClicked 函数捕获并显示错误信息

    def fill_grid(self, grid_obj, data, font_size, row_height, is_first_grid=False, custom_renderer=None):
        if not grid_obj:
            return

        try:
            df_processed = data.copy()
            if not df_processed.empty:
                # 再次处理空值和移除空行/列，确保传递给 Grid 的数据是干净的
                df_processed = df_processed.applymap(lambda x: '' if pd.isna(x) or x is None else x)
                df_processed = df_processed.loc[~(df_processed == '').all(axis=1)]
                df_processed = df_processed.loc[:, ~(df_processed == '').all(axis=0)]

            data_to_display = df_processed.values.tolist()# 将 DataFrame 转换为列表形式，方便遍历

            # 计算 Grid 的目标行和列数
            target_rows, target_cols, num_data_rows, num_data_cols = calculate_target_dimensions(
                df_processed, self.GLOBAL_MIN_ROWS, self.GLOBAL_MIN_COLUMNS
            )

            current_rows = grid_obj.GetNumberRows()
            current_cols = grid_obj.GetNumberCols()

            #在更新前暂停 Grid 绘制
            grid_obj.BeginBatch()

            # 调整 Grid 的行数以匹配目标行数
            if target_rows > current_rows:
                grid_obj.AppendRows(target_rows - current_rows)
            elif target_rows < current_rows:
                grid_obj.DeleteRows(target_rows, current_rows - target_rows)

            # 调整 Grid 的列数以匹配目标列数
            if target_cols > current_cols:
                grid_obj.AppendCols(target_cols - current_cols)
            elif target_cols < current_cols:
                grid_obj.DeleteCols(target_cols, current_cols - target_cols)

            # 设置 Grid 的默认样式属性
            adjusted_font = wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            grid_obj.SetDefaultCellFont(adjusted_font)# 设置默认字体
            grid_obj.SetDefaultRowSize(row_height)# 设置默认行高
            grid_obj.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)# 设置默认单元格内容居中对齐

            grid_obj.EnableGridLines(True)# 启用网格线
            # 设置所有 Grid 的默认网格线颜色为浅灰色，这会影响没有自定义渲染器的单元格
            grid_obj.SetGridLineColour(wx.Colour(200, 200, 200))

            # 计算数据在 Grid 中居中显示的偏移量
            row_offset = (target_rows - num_data_rows) // 2
            col_offset = (target_cols - num_data_cols) // 2

            row_offset = max(0, row_offset)
            col_offset = max(0, col_offset)

            # 遍历数据并填充到 Grid 单元格
            for r_idx, row_data in enumerate(data_to_display):
                for c_idx, cell_value in enumerate(row_data):
                    target_r = r_idx + row_offset# 实际 Grid 行索引
                    target_c = c_idx + col_offset# 实际 Grid 列索引

                    if target_r < target_rows and target_c < target_cols:# 确保索引在 Grid 范围内
                        formatted_value = ''
                        is_cell_empty = True
                        if cell_value != '':# 如果单元格值不为空
                            is_cell_empty = False
                            try:
                                num_value = float(cell_value)
                                # 尝试将浮点数转换为整数（如果它实际上是整数，例如 10.0 显示为 10）
                                if abs(num_value - round(num_value)) < 1e-9:
                                    formatted_value = str(int(round(num_value)))
                                else:
                                    formatted_value = str(num_value)# 否则保留浮点数格式
                            except ValueError:
                                formatted_value = str(cell_value) # 如果不是数字，则直接转换为字符串

                        grid_obj.SetCellValue(target_r, target_c, formatted_value)# 设置单元格值

                        # --- 每次填充前，先确保单元格恢复到默认状态 ---
                        # 确保单元格没有自定义渲染器，这样它会使用Grid的默认网格线。
                        grid_obj.SetCellRenderer(target_r, target_c, None)
                        # 默认背景色设置为白色
                        grid_obj.SetCellBackgroundColour(target_r, target_c, wx.WHITE)

                        if is_first_grid and not is_cell_empty:
                            #用于设置第一个grid的单元格边框
                            #grid_obj.SetCellRenderer(target_r, target_c, custom_renderer)
                            #如果是第一个 Grid (m_gridStructuralUnitID) 且单元格有数据，则设置背景色为绿色
                            grid_obj.SetCellBackgroundColour(target_r, target_c, wx.GREEN)

            grid_obj.ForceRefresh() # 结束批量操作，一次性绘制所有更改
            grid_obj.Update() # 更新窗口
            grid_obj.SetMinSize(wx.Size(1, 1))# 再次设置最小尺寸，确保布局计算正确

        except Exception as e:
            print(f"Error in fill_grid for grid_obj: {grid_obj.GetName() if grid_obj else 'None'}. Error: {e}")
            import traceback
            traceback.print_exc()
            if grid_obj:
                grid_obj.SetMinSize(wx.Size(100, 100))# 异常时设置一个默认最小尺寸
                grid_obj.EndBatch()  # 确保在异常发生时也结束批量操作
                raise  # 重新抛出异常，让上层函数 (load_excel_data_and_populate_grids) 处理

    def finalize_all_grid_column_widths(self, grid_list, max_cols_overall):
        if not grid_list or max_cols_overall == 0:
            # 如果没有 Grid 或没有列，则直接进行布局调整并返回
            self.bSizerGridsContent.Layout()
            self.m_scrolledGridPanel.SetVirtualSize(self.bSizerGridsContent.GetMinSize())
            self.m_scrolledGridPanel.SetMinSize(self.bSizerGridsContent.GetMinSize())
            self.m_scrolledGridPanel.Layout()
            self.Layout()
            self.Fit()
            return

        panel_client_width = self.m_scrolledGridPanel.GetClientSize().GetWidth()

        # 计算 Grid 内容的可用宽度，减去边距填充
        GRID_CONTENT_AVAILABLE_WIDTH = panel_client_width - 40

        if GRID_CONTENT_AVAILABLE_WIDTH <= 0:
            print(
                f"Warning: Calculated GRID_CONTENT_AVAILABLE_WIDTH is zero or negative ({GRID_CONTENT_AVAILABLE_WIDTH}). Retrying finalize_all_grid_column_widths later.")
            # 如果可用宽度为非正数，则稍后重试，这可能发生在窗口刚创建时
            wx.CallAfter(self.finalize_all_grid_column_widths, grid_list, max_cols_overall)
            return

        for grid_obj in grid_list:
            current_grid_cols = grid_obj.GetNumberCols()
            if current_grid_cols == 0:
                continue # 如果当前 Grid 没有列，则跳过

            # 计算基础列宽和余数，将可用宽度均匀分配给列
            base_width_for_this_grid = max(self.MIN_CELL_WIDTH, GRID_CONTENT_AVAILABLE_WIDTH // current_grid_cols)
            remainder_for_this_grid = GRID_CONTENT_AVAILABLE_WIDTH % current_grid_cols

            total_grid_width_set = 0
            for c_idx in range(current_grid_cols):
                col_size = base_width_for_this_grid
                if c_idx < remainder_for_this_grid:
                    col_size += 1 # 将余数均匀分配给前几列

                final_col_size = max(self.MIN_CELL_WIDTH, col_size) # 确保列宽不小于最小宽度
                grid_obj.SetColSize(c_idx, final_col_size) # 设置列宽
                total_grid_width_set += final_col_size

            # 计算 Grid 的总高度（行高 * 行数 + 列标题高度）
            calculated_grid_total_height = grid_obj.GetNumberRows() * grid_obj.GetDefaultRowSize() + grid_obj.GetColLabelSize()

            # 设置 Grid 的最小尺寸，以便 Sizer 能够正确管理其大小
            grid_obj.SetMinSize(wx.Size(total_grid_width_set, calculated_grid_total_height))

            grid_obj.ForceRefresh()# 强制刷新显示
            grid_obj.Update() # 更新窗口

        # 再次布局和调整滚动面板及对话框的尺寸，确保所有 Grid 都已调整完毕
        self.bSizerGridsContent.Layout()
        self.m_scrolledGridPanel.SetVirtualSize(self.bSizerGridsContent.GetMinSize())
        self.m_scrolledGridPanel.SetMinSize(self.bSizerGridsContent.GetMinSize())
        self.m_scrolledGridPanel.Layout()

        self.Layout()
        self.Fit()

    def OnStartImportClicked(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()

    def OnApplyClicked(self, event):
        wx.MessageBox("数据已应用！", "提示", wx.OK | wx.ICON_INFORMATION)
        event.Skip()

    def OnCancelClicked(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


if __name__ == '__main__':
    app = wx.App()
    dialog = ExportFibersim(None)
    dialog.ShowModal()
    dialog.Destroy()
    app.MainLoop()