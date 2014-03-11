﻿using SeniorProject;

namespace SeniorProjectTests
{
    class MockEntity: ICompressible
    {
        private double complexity;
        private byte[] data;

        public MockEntity()
        {
            data = null;
            complexity = 0;
        }

        public MockEntity(byte[] data)
        {
            this.data = data;
            complexity = 0;
        }

        byte[] ICompressible.ToByteArray()
        {
            return data;
        }

        double ICompressible.Complexity
        {
            get { return this.complexity; }
            set { this.complexity = value;}
        }
    }
}
