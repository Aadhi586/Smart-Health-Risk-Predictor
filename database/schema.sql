USE [HealthAppDB]
GO
/****** Object:  Table [dbo].[HealthData]    Script Date: 26-06-2026 20:50:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HealthData](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[username] [varchar](100) NULL,
	[height] [float] NULL,
	[weight] [float] NULL,
	[bmi] [float] NULL,
	[diabetes] [varchar](10) NULL,
	[diabetes_value] [float] NULL,
	[bp] [varchar](10) NULL,
	[bp_value] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[HealthDetails]    Script Date: 26-06-2026 20:50:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HealthDetails](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[username] [varchar](50) NULL,
	[height] [float] NULL,
	[weight] [float] NULL,
	[bmi] [float] NULL,
	[diabetes] [bit] NULL,
	[diabetes_level] [float] NULL,
	[bp] [bit] NULL,
	[systolic] [float] NULL,
	[diastolic] [float] NULL,
	[stress_level] [int] NULL,
	[alcohol_level] [int] NULL,
	[smoking_level] [int] NULL,
	[created_at] [datetime] NULL,
	[risk_percentage] [float] NULL,
	[location] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 26-06-2026 20:50:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](100) NULL,
	[username] [varchar](50) NULL,
	[dob] [date] NULL,
	[email] [varchar](100) NULL,
	[password] [varchar](255) NULL,
	[temp_password] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[HealthDetails] ADD  DEFAULT (getdate()) FOR [created_at]
GO
