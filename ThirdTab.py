class ThirdTab:
	def createThirdTab(self, ttk, tab3):
		self.entry = ttk.Entry(self.tab3, width=10).grid(row=0, column=0, sticky='e', padx = 5, pady = 5);
		self.tab3.columnconfigure(0, weight=1)

